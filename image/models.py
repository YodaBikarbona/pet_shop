from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class Image(models.Model):

    FORMAT_CHOICES = [
        ("jpg", "JPG"),
        ("jpeg", "JPEG"),
    ]

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    name = models.CharField(max_length=64)
    path = models.CharField(max_length=255)
    format = models.CharField(max_length=4, choices=FORMAT_CHOICES)

    def __str__(self):
        return f"{self.name}.{self.format}"

    def save(self, *args, **kwargs):
        if self.format not in dict(self.FORMAT_CHOICES).keys():
            raise ValidationError("Invalid format!")
        super().save(*args, **kwargs)
