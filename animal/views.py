import logging

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from animal.models import Animal
from animal.queries import (
    get_all_animals,
    get_animal_by_id,
)
from animal.serializers import (
    AnimalSerializer,
    NewAnimalSerializer,
    EditAnimalSerializer,
)
from category.queries import get_category_by_id
from mark.queries import get_mark_by_id
from pet_shop.error_messages import *
from pet_shop.ok_messages import *

logger = logging.getLogger(__name__)


class AnimalListApiView(APIView):

    @extend_schema(
        methods=["get"],
        description=f"""
            - An endpoint to retrieve all existing animals.
            - If there is no animals it will return an error 404 - {ANIMALS_NOT_FOUND}
            """,
        responses={
            200: AnimalSerializer(many=True),
            404: {"description": ANIMALS_NOT_FOUND},
        },
    )
    def get(self, request, *args, **kwargs):

        animals = get_all_animals()
        if not animals:
            return Response(ANIMALS_NOT_FOUND, status=404)
        response = AnimalSerializer(instance=animals, many=True).data

        return Response(data=response, status=200)


class NewAnimalApiView(APIView):

    @extend_schema(
        methods=["post"],
        description=f"""
            - An endpoint to create new animal.
            - If one of the body data is wrong or some relation field doesn't exist 
            it will return an error 400 - {WRONG_DATA}
            """,
        request=NewAnimalSerializer(many=False),
        responses={
            201: {"description": ANIMAL_SUCCESSFULLY_CREATED},
            400: {"description": WRONG_DATA},
        },
    )
    def post(self, request, *args, **kwargs):

        data = NewAnimalSerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(WRONG_DATA, status=400)

        category = get_category_by_id(_id=data.validated_data.get("category_id"))
        if not category:
            logger.error(f"The category {data.validated_data.get("category_id")} doesn't exist!")
            return Response(WRONG_DATA, status=400)

        mark = get_mark_by_id(_id=data.validated_data.get("mark_id"))
        if not mark:
            logger.error(f"The mark {data.validated_data.get("mark_id")} doesn't exist!")
            return Response(WRONG_DATA, status=400)

        animal = Animal(
            animal_id=data.validated_data.get("animal_id"),
            name=data.validated_data.get("name"),
            status=data.validated_data.get("status"),
            category=category,
            mark=mark,
        )
        if not animal.is_valid_status():
            logger.error(f"Invalid status: {data.validated_data.get("status")}!")
            return Response(WRONG_DATA, status=400)
        if data.duplicate_animal_id(_animal_id=data.validated_data.get("animal_id")):
            logger.error(f"Duplicate animal_id: {data.validated_data.get("animal_id")}!")
            return Response(WRONG_DATA, status=400)
        animal.save()

        return Response(ANIMAL_SUCCESSFULLY_CREATED, status=201)


class EditAnimalApiView(APIView):

    @extend_schema(
        methods=["patch"],
        description=f"""
            - An endpoint to edit existing animal (by ID - record of the animal).
            - If one of the body data is wrong or some relation field doesn't exist 
            it will return an error 400 - {WRONG_DATA}
            - If non existing animal is trying to edit it will return an error 404 - {ANIMAL_NOT_FOUND}
            """,
        request=EditAnimalSerializer(many=False),
        responses={
            204: {"description": ANIMAL_SUCCESSFULLY_EDITED},
            400: {"description": WRONG_DATA},
            404: {"description": ANIMAL_NOT_FOUND},
        },
    )
    def patch(self, request, _id, *args, **kwargs):

        data = EditAnimalSerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(WRONG_DATA, status=400)

        animal = get_animal_by_id(_id=_id)
        if not animal:
            logger.error(f"The animal {_id} doesn't exist!")
            return Response(ANIMAL_NOT_FOUND, status=404)

        category = get_category_by_id(_id=data.validated_data.get("category_id"))
        if not category:
            logger.error(f"The category {data.validated_data.get("category_id")} doesn't exist!")
            return Response(WRONG_DATA, status=400)

        mark = get_mark_by_id(_id=data.validated_data.get("mark_id"))
        if not mark:
            logger.error(f"The mark {data.validated_data.get("mark_id")} doesn't exist!")
            return Response(WRONG_DATA, status=400)

        animal.animal_id = data.validated_data.get("animal_id")
        animal.name = data.validated_data.get("name")
        animal.status = data.validated_data.get("status")
        animal.category = category
        animal.mark = mark
        if not animal.is_valid_status():
            logger.error(f"Invalid status: {data.validated_data.get("status")}!")
            return Response(WRONG_DATA, status=400)
        if data.duplicate_animal_id(_animal_id=data.validated_data.get("animal_id"), _id=animal.id):
            logger.error(f"Duplicate animal_id: {data.validated_data.get("animal_id")}!")
            return Response(WRONG_DATA, status=400)
        animal.save()

        return Response(ANIMAL_SUCCESSFULLY_EDITED, status=204)


class DeleteAnimalApiView(APIView):

    @extend_schema(
        methods=["delete"],
        description=f"""
            - An endpoint to delete existing animal (by ID - record of the animal).
            - If non existing animal is trying to delete it will return an error 404 - {ANIMAL_NOT_FOUND}.
            """,
        responses={
            204: {"description": ANIMAL_SUCCESSFULLY_DELETED},
            404: {"description": ANIMAL_NOT_FOUND},
        },
    )
    def delete(self, request, _id, *args, **kwargs):

        animal = get_animal_by_id(_id=_id)
        if not animal:
            logger.error(f"The animal {_id} doesn't exist!")
            return Response(ANIMAL_NOT_FOUND, status=404)
        animal.delete()

        return Response(ANIMAL_SUCCESSFULLY_DELETED, status=204)


class AnimalApiView(APIView):

    @extend_schema(
        methods=["get"],
        description=f"""
            - An endpoint to retrieve some specific animal (by ID - record of the animal).
            - If non existing animal is trying to retrieve it will return an error 404 - {ANIMAL_NOT_FOUND}.
            """,
        responses={
            200: AnimalSerializer(many=False),
            404: {"description": ANIMAL_NOT_FOUND},
        },
    )
    def get(self, request, _id, *args, **kwargs):

        animal = get_animal_by_id(_id=_id)
        if not animal:
            logger.error(f"The animal {_id} doesn't exist!")
            return Response(ANIMAL_NOT_FOUND, status=404)
        response = AnimalSerializer(instance=animal, many=False).data

        return Response(data=response, status=200)
