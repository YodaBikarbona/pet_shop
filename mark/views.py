import logging

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from mark.models import Mark
from mark.queries import (
    get_all_marks,
    get_mark_by_id,
)
from mark.serializers import (
    MarkSerializer,
    NewMarkSerializer,
    EditMarkSerializer,
)
from pet_shop.error_messages import *
from pet_shop.ok_messages import *

logger = logging.getLogger(__name__)


class MarkListApiView(APIView):

    @extend_schema(
        methods=["get"],
        description=f"""
            - An endpoint to retrieve all existing marks.
            - If there is no marks it will return an error 404 - {MARKS_NOT_FOUND}
            """,
        responses={
            200: MarkSerializer(many=True),
            404: {"description": MARKS_NOT_FOUND},
        },
    )
    def get(self, request, *args, **kwargs):

        marks = get_all_marks()
        if not marks:
            return Response(MARKS_NOT_FOUND, status=404)
        response = MarkSerializer(instance=marks, many=True).data

        return Response(data=response, status=200)


class NewMarkApiView(APIView):

    @extend_schema(
        methods=["post"],
        description=f"""
            - An endpoint to create new mark.
            - If one of the body data is wrong it will return an error 400 - {WRONG_DATA}
            """,
        request=NewMarkSerializer(many=False),
        responses={
            201: {"description": MARK_SUCCESSFULLY_CREATED},
            400: {"description": WRONG_DATA},
        },
    )
    def post(self, request, *args, **kwargs):

        data = NewMarkSerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(WRONG_DATA, status=400)
        mark = Mark(
            name=data.validated_data.get("name")
        )
        if data.duplicate_mark(_name=data.validated_data.get("name")):
            logger.error(f"The mark {data.validated_data.get("name")} already exists!")
            return Response(WRONG_DATA, status=400)
        mark.save()

        return Response(MARK_SUCCESSFULLY_CREATED, status=201)


class EditMarkApiView(APIView):

    @extend_schema(
        methods=["patch"],
        description=f"""
            - An endpoint to edit existing mark (by ID - record of the mark).
            - If one of the body data is wrong it will return an error 400 - {WRONG_DATA}
            - If non existing mark is trying to edit it will return an error 404 - {MARK_NOT_FOUND}
            """,
        request=EditMarkSerializer(many=False),
        responses={
            204: {"description": MARK_SUCCESSFULLY_EDITED},
            400: {"description": WRONG_DATA},
            404: {"description": MARK_NOT_FOUND},
        },
    )
    def patch(self, request, _id, *args, **kwargs):

        data = EditMarkSerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(data=WRONG_DATA, status=400)

        mark = get_mark_by_id(_id=_id)
        if not mark:
            logger.error(f"The mark {_id} doesn't exist!")
            return Response(data=MARK_NOT_FOUND, status=404)
        mark.name = data.validated_data.get("name")
        if data.duplicate_mark(_name=data.validated_data.get("name"), _id=mark.id):
            logger.error(f"The mark {data.validated_data.get("name")} already exists!")
            return Response(WRONG_DATA, status=400)
        mark.save()

        return Response(MARK_SUCCESSFULLY_EDITED, status=204)


class DeleteMarkApiView(APIView):

    @extend_schema(
        methods=["delete"],
        description=f"""
            - An endpoint to delete existing mark (by ID - record of the mark).
            - If non existing mark is trying to delete it will return an error 404 - {MARK_NOT_FOUND}.
            """,
        responses={
            204: {"description": MARK_SUCCESSFULLY_DELETED},
            404: {"description": MARK_NOT_FOUND},
        },
    )
    def delete(self, request, _id, *args, **kwargs):

        mark = get_mark_by_id(_id=_id)
        if not mark:
            logger.error(f"The mark {_id} doesn't exist!")
            return Response(data=MARK_NOT_FOUND, status=404)
        mark.delete()

        return Response(MARK_SUCCESSFULLY_DELETED, status=204)


class MarkApiView(APIView):

    @extend_schema(
        methods=["get"],
        description=f"""
            - An endpoint to retrieve some specific mark (by ID - record of the mark).
            - If non existing mark is trying to retrieve it will return an error 404 - {MARK_NOT_FOUND}.
            """,
        responses={
            200: MarkSerializer(many=False),
            404: {"description": MARK_NOT_FOUND},
        },
    )
    def get(self, request, _id, *args, **kwargs):

        mark = get_mark_by_id(_id=_id)
        if not mark:
            logger.error(f"The mark {_id} doesn't exist!")
            return Response(data=MARK_NOT_FOUND, status=404)
        response = MarkSerializer(instance=mark, many=False).data

        return Response(data=response, status=200)
