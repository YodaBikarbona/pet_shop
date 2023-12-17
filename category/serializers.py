from rest_framework import serializers
from rest_framework.fields import CharField

from category.models import Category
from category.queries import get_category_by_name


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "created_at",
            "modified_at",
            "name",
        ]


class NewCategorySerializer(serializers.Serializer):

    name: CharField = serializers.CharField(help_text="The name of the category")

    def duplicate_category(self, _name: str, _id: int = None) -> bool:
        category = get_category_by_name(_name=_name)
        if category and _id and category.id == _id:
            return False
        if not _id and not category:
            return False
        if _id and not category:
            return False
        return True


class EditCategorySerializer(NewCategorySerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
