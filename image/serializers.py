from rest_framework import serializers
from rest_framework.fields import (
    ImageField,
    IntegerField,
)


class NewImageSerializer(serializers.Serializer):

    image: ImageField = serializers.ImageField(help_text="The image of the animal")
    id: IntegerField = serializers.IntegerField(help_text="The ID of the animal record")
