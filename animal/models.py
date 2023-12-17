from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from category.models import Category
from image.models import Image
from mark.models import Mark


class Animal(models.Model):

    STATUS_CHOICES = [
        ("set", "Set"),
        ("approved", "Approved"),
        ("delivered", "Delivered"),
    ]

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)
    animal_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=32)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    mark = models.ForeignKey(Mark, on_delete=models.SET_NULL, null=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.animal_id} - {self.name}"

    def is_valid_status(self) -> bool:
        """
        Check is chosen status valid
        :return: bool
        """
        if self.status not in dict(self.STATUS_CHOICES).keys():
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.is_valid_status():
            raise ValidationError("Invalid status!")
        super().save(*args, **kwargs)
