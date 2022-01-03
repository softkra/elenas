from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.db.models import  BooleanField, CharField, TextField, ForeignKey, CASCADE
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Create your models here.
class Tasks(TimeStampedModel, SoftDeletableModel):

    """Model for managing Tasks

    Attributes:
        title: Task title
        description: Task description
        is_completed: Task status
        user: Owner
    """

    title = CharField(max_length=255)
    description = TextField(verbose_name=_('Descripcion de la tarea'))
    is_completed = BooleanField(default=False, verbose_name=_('¿Esta completa?'))
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name="Usuario"
    )