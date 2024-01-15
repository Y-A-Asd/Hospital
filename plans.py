from abc import ABC, abstractmethod



class Plan(ABC):
    @abstractmethod
    def get_plan(self):
        pass

    def __str__(self):
        return str(self.get_plan().lower().split()[0])


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

