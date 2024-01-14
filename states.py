from abc import ABC, abstractmethod
from __future__ import annotations
from transitions import Machine

from models import Patient


class Context:
    def __init__(self, state):
        self.go(state)

    def go(self, state):
        self._state = state
        self._state.context = self

    def discharge(self):
        self._state.discharge()

    def charge(self):
        self._state.charge()

    def add_patient(self):
        self._state.add_patient()

    def get_log(self):
        return self._state.get_log()


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
    def charge(self):
        pass

    @abstractmethod
    def add_patient(self):
        pass

    @abstractmethod
    def get_log(self):
        pass


class Enter(State):
    def discharge(self):
        self.context.go(Discharged())

    def charge(self):
        self.context.go(Charged())

    def add_patient(self):
        # Implementation for adding a patient in the 'Enter' state
        pass

    def get_log(self):
        # Implementation for getting log in the 'Enter' state
        pass


class Charged(State):
    def discharge(self):
        self.context.go(Discharged())

    def charge(self):
        self.context.go(Charged())

    def add_patient(self):
        # Implementation for adding a patient in the 'Charged' state
        pass

    def get_log(self):
        # Implementation for getting log in the 'Charged' state
        pass


class Discharged(State):
    def discharge(self):
        # Implementation for discharging in the 'Discharged' state
        pass

    def charge(self):
        self.context.go(Charged())

    def add_patient(self):
        # Implementation for adding a patient in the 'Discharged' state
        pass

    def get_log(self):
        # Implementation for getting log in the 'Discharged' state
        pass


class HospitalManager:

    states = ['Discharged', 'Charged', 'Enter']

    transitions = [
        {'trigger': 'enter', 'source': 'Enter', 'dest': 'Charged'},
        {'trigger': 'outpatients', 'source': 'Enter', 'dest': 'Discharged'},
        {'trigger': 'treatment', 'source': 'Charged', 'dest': 'Discharged'},
        {'trigger': 'reappearance', 'source': 'Discharged', 'dest': 'Charged'},
    ]

    def __init__(self, patient: Patient):

        machine = Machine(patient, states=self.states, transitions=self.transitions, initial='Enter')

# hm = HospitalManager(...)
# hm.state
# hm.[trigger]