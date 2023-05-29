import uuid
from django.db import models
from apps.authentication.models import User


class BaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_created',
                                   on_delete=models.PROTECT)
    modified_by = models.ForeignKey(User, null=True, editable=False, related_name='%(class)s_modified',
                                    on_delete=models.PROTECT)

    class Meta:
        abstract = True
