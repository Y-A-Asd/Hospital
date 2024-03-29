import datetime
from typing import Optional
from tortoise.expressions import F
import tortoise
from tortoise.models import Model
from tortoise import fields, BaseDBAsyncClient
from tortoise.manager import Manager
from tortoise import Tortoise
import asyncio
from tortoise import run_async
from tortoise.contrib.pydantic import pydantic_model_creator

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted_at__isnull=True)


class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(null=True)
    all_obj = Manager()

    async def delete(self, using_db=None) -> None:
        self.deleted_at = datetime.datetime.now()
        await self.save()

    class Meta:
        manager = SoftDeleteManager()
        abstract = True
        ordering = ('-created_at',)


class Patient(BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    age = fields.IntField()
    gender = fields.CharField(max_length=31)
    birthday = fields.DatetimeField()
    all_obj = Manager()

    class Meta:
        ordering = ['-created_at']
        indexes = ('id', 'name')
        manager = SoftDeleteManager()

    def __str__(self):
        return f'Name: {self.name} - Age: {self.age} Gender: {self.gender}'


Patient_Pydantic = pydantic_model_creator(Patient, name='Patient')


class Hospital(BaseModel):
    """
    Plans:
        Full insurance
        health insurance
        no insurance
    """
    id = fields.IntField(pk=True)
    plan_name = fields.CharField(max_length=255, null=True)
    person = fields.ForeignKeyField('models.Patient', related_name='patient')
    status = fields.CharField(max_length=255)
    pay = fields.DecimalField(max_digits=16, decimal_places=2, default=0.0)
    all_obj = Manager()

    class Meta:
        ordering = ['-created_at']
        indexes = ('person', 'status')
        manager = SoftDeleteManager()



Hospital_Pydantic = pydantic_model_creator(Hospital, name='Hospital')


class Reservation(BaseModel):
    id = fields.IntField(pk=True)
    person = fields.ForeignKeyField('models.Patient', related_name='person')
    status = fields.CharField(max_length=255)
    date = fields.DateField()
    all_obj = Manager()

    def __str__(self):
        return f'Reservation for {self.person} at {self.date} {{{self.status}}}'
    class Meta:
        ordering = ['-created_at']
        indexes = ('id', 'date')
        manager = SoftDeleteManager()


async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )

    await Tortoise.generate_schemas()

# await init()
# func = init()
# asyncio.run(func)
# run_async(init_db())
