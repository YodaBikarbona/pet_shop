from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.fields import (
    CharField,
    IntegerField,
)

from animal.models import Animal
from animal.queries import get_animal_by_animal_id
from category.models import Category
from image.models import Image
from mark.models import Mark


class AnimalCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class AnimalMarkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Mark
        fields = [
            "id",
            "name",
        ]


class AnimalImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = [
            "id",
            "path",
        ]


class AnimalSerializer(serializers.HyperlinkedModelSerializer):
    category = AnimalCategorySerializer(many=False)
    mark = AnimalMarkSerializer(many=False)
    image = AnimalImageSerializer(many=False)

    class Meta:
        model = Animal
        fields = [
            "id",
            "created_at",
            "modified_at",
            "animal_id",
            "name",
            "status",
            "category",
            "mark",
            "image",
        ]


class NewAnimalSerializer(serializers.Serializer):

    animal_id: IntegerField = serializers.IntegerField(
        validators=[MinValueValidator(1)], help_text="The number of the animal, this field is unique for some animal")
    name: CharField = serializers.CharField(help_text="The name of the animal, e.g. Max")
    status: CharField = serializers.CharField(help_text="The status of the animal, could be set/approved/delivered")
    category_id: IntegerField = serializers.IntegerField(
        validators=[MinValueValidator(1)], help_text="ID of some specific category")
    mark_id: IntegerField = serializers.IntegerField(
        validators=[MinValueValidator(1)], help_text="ID of some specific mark")

    def duplicate_animal_id(self, _animal_id: int, _id: int = None) -> bool:
        animal = get_animal_by_animal_id(_animal_id=_animal_id)
        if animal and _id and animal.id == _id:
            return False
        if not _id and not animal:
            return False
        return True


class EditAnimalSerializer(NewAnimalSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
