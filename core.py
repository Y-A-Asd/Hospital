from abc import ABC, abstractmethod

from views import State


class Plan(ABC):
    @abstractmethod
    def get_plan(self):
        pass


class FullInsurancePlan(Plan):
    off = 20

    def get_plan(self):
        return "Full Insurance Plan"


class HealthInsurancePlan(Plan):
    off = 5

    def get_plan(self):
        return "Health Insurance Plan"


class NoInsurancePlan(Plan):
    off = 0

    def get_plan(self):
        return "No Insurance Plan"


class PlanFactory:
    @staticmethod
    def create_plan(plan_type):
        plan_class_name = plan_type.capitalize() + 'InsurancePlan'

        try:
            plan_class = globals()[plan_class_name]
        except KeyError:
            raise ValueError("Invalid plan type")

        return plan_class()


# a = PlanFactory.create_plan("full")
# print(a.off)


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
        self.context.go(Discharge)

    def charge(self):
        self.context.go(Charge)

    def add_patient(self):
        ...

    def get_log(self):
        self._state.get_log


class Charge(State):
    ...


class Discharge(State):
    ...
