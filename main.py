import asyncio

from models import Patient
from plans import PlanManager
from routes import BaseMenu
from tortoise import Tortoise
from reserve import ReservationManager
from states import HospitalManager


# async def main():
#     await Tortoise.init(
#         db_url='sqlite://db.sqlite3',
#         modules={'models': ['models']}
#     )
#
#     reservation_manager = ReservationManager()
#     await reservation_manager.menu()
#
#
# asyncio.run(main())


class BaseMenuGenerator(BaseMenu):
    def __init__(self):
        self.hospital= None
        manager_name = "Wellcome"
        menu_items = [
            {"label": "Enter Patient", "action": self.addingpatient, "args": ['name', 'age', 'gender', 'birthday']},
            {"label": "Select Patient", "action": self.selectpatient, "args": ['name']},
            {"label": "View Current Pay", "action": self.current_pay, "args": []},
            {"label": "Add Pay", "action": self.current_pay, "args": ["amount"]},
            {"label": "Get Plan", "action": self.get_plan, "args": []},
            {"label": "Exit", "action": self.exit_program, "args": []},
        ]

    async def addingpatient(self,name, age, gender, birthday):
        patient = Patient(name=name, age=age, gender=gender, birthday=birthday)
        plan = asyncio.run(PlanManager())
        self.hospital = HospitalManager(patient, plan, 0)
        await asyncio.sleep(0.5)

    async def selectpatient(self,name):
        patient = await Patient.get_or_none(name__contains=name)
        # plan = asyncio.run(PlanManager())
        self.hospital = HospitalManager(patient, plan, 0)




