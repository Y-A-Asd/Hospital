import asyncio
from tortoise import Tortoise, run_async
from models import Patient, Reservation
from routes import BaseMenu


class ReservationManager(BaseMenu):
    def __init__(self):
        # asyncio.run(self.init_db())
        manager_name = "Reservation"
        menu_items = [
            {"label": "Add Reservation", "action": self.add_reservation, "args": ["name", "date"]},
            {"label": "Delete Reservation", "action": self.delete_reservation, "args": ["id"]},
            {"label": "List Reservations", "action": self.list_reservations, "args": []},
            {"label": "Exit", "action": ..., "args": []},
        ]
        super().__init__(manager_name, menu_items)

    # async def init_db(self):
    #     await Tortoise.init(
    #         db_url='sqlite://db.sqlite3',
    #         modules={'models': ['__main__']}
    #     )
    #     await asyncio.sleep(2)

    async def add_reservation(self, name, status: 'waiting', date):
        person = await Patient.get_or_none(name=name)
        if person:
            await Reservation.create(person=person, status=status, date=date)
            print("Reservation added.")
        else:
            print("Patient not found.")

    async def delete_reservation(self, id):
        reservation = await Reservation.get_or_none(id=id)
        if reservation:
            await reservation.delete()
            print("Reservation deleted.")
        else:
            print("Reservation not found.")

    async def list_reservations(self):
        reservations = await Reservation.all()
        if reservations:
            print("Reservations:")
            for reservation in reservations:
                print(f"- {reservation}")
        else:
            print("No reservations found.")
