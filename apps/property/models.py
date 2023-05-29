from apps.authentication.models import User
from apps.core.models import BaseModel, models


class Property(BaseModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    bio = models.TextField(blank=True, null=True)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True, related_name='tenant')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=False, null=False, related_name='property_owner')

    def __str__(self):
        return self.name
