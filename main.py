import asyncio
import sys
from models import Patient, Hospital
from plans import PlanManager
from routes import BaseMenu
from tortoise import Tortoise
from states import HospitalManager





class BaseMenuGenerator(BaseMenu):
    def __init__(self):
        self.hospital = None
        manager_name = "Wellcome"
        menu_items = [
            {"label": "Enter Patient", "action": self.addingpatient, "args": ['name', 'age', 'gender', 'birthday']},
            {"label": "Select Patient", "action": self.selectpatient, "args": ['name']},
            {"label": "Exit", "action": self.exit, "args": []},
        ]
        super().__init__(manager_name, menu_items)
    # async def menu(self):
    #     await self.router.menu(self.manager_name, self.menu_items)

    async def addingpatient(self, name, age, gender, birthday):
        patient = Patient.create(name=name, age=age, gender=gender, birthday=birthday)
        plan = await PlanManager()
        self.hospital = HospitalManager(patient, plan, 0)
        # await asyncio.sleep(2.5)
        # print(self.hospital)

    async def selectpatient(self, name):
        patient = await Patient.get_or_none(name__contains=name)
        hospital = Hospital.get_or_none(person=patient, status__not='discharged')
        print(hospital)
        # plan = asyncio.run(PlanManager())
        # self.hospital = HospitalManager(patient, plan, 0)

    async def exit(self):
        await Tortoise.close_connections()
        sys.exit('Y.A.A')


async def main():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )

    ma = BaseMenuGenerator()
    await ma.menu()



asyncio.run(main())
