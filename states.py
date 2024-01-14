from abc import ABC, abstractmethod

class Context:
    -state = None

    def __init__(self, state: State):
        self.go(state)

    def go(self, state: State):
        self._state = state
        self._state.context = self

    def discharge(self):
        self._state.discharge

    def charge(self):
        self._state.charge

    def add_patient(self):
        self._state.add_patient

    def get_log(self):
        self._state.get_log


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def discharge(self):
        self._state.discharge

    @abstractmethod
    def charge(self):
        self._state.charge

    @abstractmethod
    def add_patient(self):
        self._state.add_patient

    @abstractmethod
    def get_log(self):
        self._state.get_log


class Enter(State):

    def discharge(self):
        self.context.go(Discharged)

    def charge(self):
        self.context.go(Charged)

    def add_patient(self):
        ...

    def get_log(self):
        ...


class Charged(State):
    ...


class Discharged(State):
    ...
