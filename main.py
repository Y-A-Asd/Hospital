import asyncio
import sys
from models import Patient, Hospital, Reservation
from plans import PlanManager
from routes import BaseMenu
from tortoise import Tortoise
from states import HospitalManager
from reserve import ReservationManager


class BaseMenuGenerator(BaseMenu):
    def __init__(self):
        self.hospital = None
        self.patient = None
        manager_name = "Wellcome"
        menu_items = [
            {"label": "Enter Patient", "action": self.addingpatient, "args": ['name', 'age', 'gender', 'birthday']},
            {"label": "Select Patient", "action": self.selectpatient, "args": ['name']},
            {"label": "Search Patient", "action": self.searchpatient, "args": ['name']},
            {"label": "Change_status", "action": self.change_status, "args": ['status', 'section']},
            {"label": "Get_status", "action": self.get_status, "args": []},
            {"label": "Add_pay", "action": self.add_pay, "args": ['pay']},
            {"label": "Reservation", "action": self.reservation, "args": []},
            {"label": "Exit", "action": self.exit, "args": []},
        ]
        super().__init__(manager_name, menu_items)

    # async def menu(self):
    #     await self.router.menu(self.manager_name, self.menu_items)

    async def addingpatient(self, name, age, gender, birthday):
        self.patient = await Patient.create(name=name, age=age, gender=gender, birthday=birthday)
        plan = await PlanManager()
        self.hospital: HospitalManager = HospitalManager(self.patient)
        await self.hospital.init_hospital(self.patient)
        await asyncio.sleep(2.5)

    async def selectpatient(self, name):
        self.patient = await Patient.get_or_none(name__contains=name)
        self.hospital = HospitalManager(self.patient)
        await self.hospital.init_hospital(self.patient)

        # plan = asyncio.run(PlanManager())

    async def searchpatient(self, name):
        self.patient = await Patient.get_or_none(name__contains=name)
        if self.patient:
            rows = await Hospital.all().filter(person=self.patient).values('person__name', 'plan_name', 'status', 'pay')
            for row in rows:
                print(row)
        else:
            print('No person found!')

    async def change_status(self, status, section: str):
        if not self.hospital:
            print('Select person first!')

        else:
            if section:
                await self.hospital.charge(section.capitalize())
            else:
                await self.hospital.discharge()

    async def get_status(self):
        patient = await Hospital.get(person=self.patient, status__not='discharged')
        print(f'Name: {patient.person}'
              f'\n Pay: {patient.pay}, Status: {patient.status}')

    async def add_pay(self, pay):
        self.hospital.current_pay = pay

    async def reservation(self):
        reservation = ReservationManager()
        await reservation.menu()

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
