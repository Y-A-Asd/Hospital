from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from tortoise import Tortoise, run_async
from transitions import Machine
from transitions.extensions import states

from log import LogMixin
from models import Patient, Hospital
import asyncio

from plans import PlanFactory, GetPlan
from routes import BaseMenu


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
        print('Discharging Person')
        self.context.go(Discharged())

    def charge(self, section):
        print(f'Person charged into {{ {section} }} section')
        self.context.go(Charged(section))

    def __str__(self):
        return 'Enter State'


class Charged(State):
    def __init__(self, section=None):
        self.section = section

    def discharge(self):
        print('Discharging Person')
        self.context.go(Discharged())

    def charge(self, section):
        print(f'Person charged from {{ {self.section} }} section -> {{ {section} }} section')
        self.context.go(Charged(section))

    def __str__(self):
        return 'Charged State'


class Discharged(State):
    def discharge(self):
        print('Person allready discharged')

    def charge(self, section:str):
        print(f'Person charged into {{ {section} }} section')
        self.context.go(Charged(section))

    def __str__(self):
        return 'Discharged State'




class HospitalManager(BaseMenu):
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

    def __init__(self, patient: Patient, plan_name: str, pay: int):
        manager_name = "Hospital Manager"
        menu_items = [
            {"label": "Discharge Patient", "action": self.discharge, "args": []},
            {"label": "Charge Patient", "action": self.charge, "args": ["section"]},
            {"label": "View Current State", "action": self.current_state, "args": []},
            {"label": "View Current Pay", "action": self.current_pay, "args": []},
            {"label": "Add Pay", "action": self.current_pay, "args": ["amount"]},
            {"label": "Get Plan", "action": self.get_plan, "args": []},
            {"label": "Exit", "action": self.exit_program, "args": []},
        ]

        super().__init__(manager_name, menu_items)
        self.hospital_manager = HospitalManager(patient, plan_name, pay)
        self.hospital = None
        self.patient = patient
        self.context = None
        asyncio.create_task(self.init_hospital(patient, plan_name, pay))

    async def init_hospital(self, patient: Patient, plan_name: str, pay: int):
        self.hospital = await Hospital.get(id=1)
        print('we are here')
        state_string = self.hospital.status.capitalize()
        state_class =getattr(sys.modules[__name__], state_string, None)
        if state_class is None or not issubclass(state_class, State):
            state_class = Enter
        print(state_class)
        self.context = Context(state_class())

    async def discharge(self):
        await asyncio.sleep(2)
        self.hospital.status = 'discharged'
        await self.hospital.save()
        self.context.discharge()

    async def charge(self, section:str):
        await asyncio.sleep(2)
        patient_info = f"Patient Info: {self.patient}"
        self.hospital.status = 'charged'
        await self.hospital.save()
        self.context.log(patient_info)
        self.context.charge(section)


    @property
    def current_state(self):
        return self.context._state

    @property
    def current_pay(self):
        return self.hospital.pay

    @current_pay.setter
    def current_pay(self, new: int):
        self.hospital.pay += new
        asyncio.create_task(self.save_pay())
    async def save_pay(self):
        await self.hospital.save()

async def main():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )

    # patient = Patient(name='test', age='20', gender='male', birthday='1970-01-01')
    # await patient.save()
    # print(patient)




    plan = PlanFactory.create_plan("full")
    # patient = await Patient.get_or_none(name='test')
    # hospital_manager = HospitalManager(patient, plan, 15000)
    # await asyncio.sleep(2)
    # # print(sys.modules[__name__].__dir__())
    # print('START')
    # print(patient)
    # print(hospital_manager.current_state)
    # await hospital_manager.charge('Kids')
    # print(hospital_manager.current_state)
    # print(hospital_manager.current_state.section)
    # print(hospital_manager.current_pay)
    # hospital_manager.current_pay = 1000
    # print(hospital_manager.current_pay)
    # await hospital_manager.charge('Brain')
    # print(hospital_manager.current_state)
    # print(hospital_manager.current_state.section)
    # await hospital_manager.discharge()
    # print(hospital_manager.current_state)
    # await hospital_manager.charge('Brain')
    # print(hospital_manager.current_state)
    # print(hospital_manager.current_state.section)
    # await hospital_manager.discharge()
    # print(hospital_manager.current_state)
    # print('End')
    # await Tortoise.close_connections()


asyncio.run(main())
