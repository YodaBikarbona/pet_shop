from django.db import models
from django.utils import timezone


class Mark(models.Model):

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
