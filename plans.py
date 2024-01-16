import asyncio
from abc import ABC, abstractmethod

from routes import BaseMenu


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


class GetPlan:
    def __init__(self):
        self.PLANS = ["Full insurance", "Health insurance", "No insurance"]
        self.selected_plan = None

    def select_plan(self, choice):
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.PLANS):
                self.selected_plan = self.PLANS[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def get_selected_option(self):
        return self.selected_plan

    async def display_menu(self):
        print("Plans:")
        for i, plan in enumerate(self.PLANS, start=1):
            print(f"{i}. {plan}")

async def PlanManager():
    plan_menu = GetPlan()
    await plan_menu.display_menu()
    choice = input("Enter your choice (1-3): ")
    await asyncio.to_thread(plan_menu.select_plan, choice)
    selected_plan:str = plan_menu.get_selected_option()
    print(f"Selected Plan: {selected_plan}")
    return PlanFactory.create_plan(selected_plan.lower().split()[0])

# b = asyncio.run(PlanManager())
# print(b.off)






