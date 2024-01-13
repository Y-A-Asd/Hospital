from tortoise.models import Model
from tortoise import fields
from tortoise.manager import Manager


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted_at__isnull=True)


class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now=True)
    update_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(default=None)
    all_obj = Manager()

    class Meta:
        abstract = True
        ordering = ('-created_at',)
        manager = SoftDeleteManager()


class Patient(BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']
        indexes = ('id', 'name')

    def __str__(self):
        return self.name


class Hospital(BaseModel):
    """
    Plans:
        Full insurance
        health insurance
        no insurance

    """
    id = fields.IntField(pk=True)
    plan_name = fields.CharField(max_length=255)
    person = fields.ForeignKeyField('models.Patient', related_name='patient')
    status = fields.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']
        indexes = ('person', 'stauts')
