from __future__ import annotations
from abc import ABC, abstractmethod
from tortoise import Tortoise, run_async
from transitions import Machine
from log import LogMixin
from models import Patient, Hospital
import asyncio

from plans import PlanFactory


class Context(LogMixin):
    _state = None

    def __init__(self, state, log_file='log.txt'):
        super().__init__(log_file)
        self.go(state)

    def go(self, state: State) -> None:
        self.log(f'Transition:{{ {self._state} }}-> {state}')
        self._state = state
        self._state.context = self

    def discharge(self):
        self.log(f'Discharging in state {{ {self._state} }}')
        self._state.discharge()

    def charge(self, section):
        self.log(f'Charging in state {self._state}')
        self._state.charge(section)


class State(ABC):
    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def discharge(self):
        pass

    @abstractmethod
    def charge(self, section):
        pass


class Enter(State):
    def discharge(self):
        self.context.go(Discharged())

    def charge(self, section):
        self.context.go(Charged(section))

    def __str__(self):
        return 'Enter State'


class Charged(State):
    def __init__(self, section=None):
        self.section = section

    def discharge(self):
        self.context.go(Discharged())

    def charge(self, section):
        self.context.go(Charged(section))

    def __str__(self):
        return 'Charged State'


class Discharged(State):
    def discharge(self):
        pass

    def charge(self, section):
        self.context.go(Charged(section))

    def __str__(self):
        return 'Discharged State'


class HospitalManager:
    """
        sections = ['Kids', 'Brain', 'Emergency']
        states = ['Discharged', 'Charged', 'Enter']

        transitions = [
            {'trigger': 'enter', 'source': 'Enter', 'dest': 'Charged'},
            {'trigger': 'outpatients', 'source': 'Enter', 'dest': 'Discharged'},
            {'trigger': 'treatment', 'source': 'Charged', 'dest': 'Discharged'},
            {'trigger': 'reappearance', 'source': 'Discharged', 'dest': 'Charged'},
        ]
    """

    def __init__(self, patient: Patient, plan_name, pay):
        self.hospital = None
        self.patient = patient
        self.context = Context(Enter())
        asyncio.create_task(self.init_hospital(patient, plan_name, pay))  # Use asyncio.create_task here

    async def init_hospital(self, patient, plan_name, pay):
        self.hospital = await Hospital.create(plan_name=plan_name, status='entered', pay=pay, person=patient)

    async def discharge(self):
        await asyncio.sleep(2)
        self.hospital.status = 'discharged'
        await self.hospital.save()
        self.context.discharge()

    async def charge(self, section):
        await asyncio.sleep(2)
        patient_info = f"Patient Info: {self.patient}"
        self.hospital.status = 'charged'
        await self.hospital.save()
        self.context.log(patient_info)
        self.context.charge(section)

    @property
    def current_state(self):
        return self.context._state


async def main():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )

    # patient = Patient(name='test', age='20', gender='male', birthday='1970-01-01')
    # await patient.save()
    # print(patient)

    plan = PlanFactory.create_plan("full")
    patient = await Patient.get_or_none(name='test')
    hospital_manager = HospitalManager(patient, plan, 15000)
    print(hospital_manager.current_state)

    await hospital_manager.charge('Kids')
    print(hospital_manager.current_state)
    print(hospital_manager.current_state.section)

    print(hospital_manager.current_state)

    await hospital_manager.discharge()
    print(hospital_manager.current_state)
    print('end')
    await Tortoise.close_connections()


asyncio.run(main())
