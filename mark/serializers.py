from rest_framework import serializers
from rest_framework.fields import CharField

from mark.models import Mark
from mark.queries import get_mark_by_name


class MarkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Mark
        fields = [
            "id",
            "created_at",
            "modified_at",
            "name",
        ]


class NewMarkSerializer(serializers.Serializer):

    name: CharField = serializers.CharField(help_text="The name of the mark")

    def duplicate_mark(self, _name: str, _id: int = None) -> bool:
        mark = get_mark_by_name(_name=_name)
        if mark and _id and mark.id == _id:
            return False
        if not _id and not mark:
            return False
        if _id and not mark:
            return False
        return True


class EditMarkSerializer(NewMarkSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
