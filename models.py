from tortoise.models import Model
from tortoise import fields
from tortoise.manager import Manager


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted_at__isnull=True)

class BaseModel(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now=True)
    update_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(default=None)
    all_obj = Manager()

    class Meta:
        abstract = True
        indexes = ('created_at', 'updated_at')
        ordering = ('-created_at',)
        """https://tortoise.github.io/manager.html?h=manager#usage"""
        manager = SoftDeleteManager()

class Patient(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

    def __str__(self):
        return self.name

class Hospital(Model):
    """
    Full insurance
    health insurance
    no insurance
    """
    id = fields.IntField(pk=True)
    plan_name = fields.CharField(max_length=255)
