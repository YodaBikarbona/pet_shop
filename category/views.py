import logging

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category
from category.queries import (
    get_category_by_id,
    get_all_categories,
)
from category.serializers import (
    CategorySerializer,
    NewCategorySerializer,
    EditCategorySerializer,
)
from pet_shop.error_messages import *
from pet_shop.ok_messages import *

logger = logging.getLogger(__name__)


class CategoryListApiView(APIView):

    @extend_schema(
        methods=["get"],
        description=f"""
            - An endpoint to retrieve all existing categories.
            - If there is no categories it will return an error 404 - {ANIMALS_NOT_FOUND}
            """,
        responses={
            200: CategorySerializer(many=True),
            404: {"description": CATEGORIES_NOT_FOUND},
        },
    )
    def get(self, request, *args, **kwargs):

        categories = get_all_categories()
        if not categories:
            return Response(CATEGORIES_NOT_FOUND, status=404)
        response = CategorySerializer(instance=categories, many=True).data

        return Response(data=response, status=200)


class NewCategoryApiView(APIView):

    @extend_schema(
        methods=["post"],
        description=f"""
            - An endpoint to create new category.
            - If one of the body data is wrong it will return an error 400 - {WRONG_DATA}
            """,
        request=NewCategorySerializer(many=False),
        responses={
            201: {"description": CATEGORY_SUCCESSFULLY_CREATED},
            400: {"description": WRONG_DATA},
        },
    )
    def post(self, request, *args, **kwargs):

        data = NewCategorySerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(WRONG_DATA, status=400)

        category = Category(
            name=data.validated_data.get("name")
        )
        if data.duplicate_category(_name=data.validated_data.get("name")):
            logger.error(f"The category {data.validated_data.get("name")} already exists!")
            return Response(WRONG_DATA, status=400)
        category.save()

        return Response(CATEGORY_SUCCESSFULLY_CREATED, status=201)


class EditCategoryApiView(APIView):

    @extend_schema(
        methods=["patch"],
        description=f"""
            - An endpoint to edit existing category (by ID - record of the category).
            - If one of the body data is wrong it will return an error 400 - {WRONG_DATA}
            - If non existing category is trying to edit it will return an error 404 - {CATEGORY_NOT_FOUND}
            """,
        request=EditCategorySerializer(many=False),
        responses={
            204: {"description": CATEGORY_SUCCESSFULLY_EDITED},
            400: {"description": WRONG_DATA},
            404: {"description": CATEGORY_NOT_FOUND},
        },
    )
    def patch(self, request, _id, *args, **kwargs):

        data = EditCategorySerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(WRONG_DATA, status=400)

        category = get_category_by_id(_id=_id)
        if not category:
            logger.error(f"The category {_id} doesn't exist!")
            return Response(CATEGORY_NOT_FOUND, status=404)
        category.name = data.validated_data.get("name")
        if data.duplicate_category(_name=data.validated_data.get("name"), _id=category.id):
            logger.error(f"The category {data.validated_data.get("name")} already exists!")
            return Response(WRONG_DATA, status=400)
        category.save()

        return Response(CATEGORY_SUCCESSFULLY_EDITED, status=204)


class DeleteCategoryApiView(APIView):

    @extend_schema(
        methods=["delete"],
        description=f"""
            - An endpoint to delete existing category (by ID - record of the category).
            - If non existing category is trying to delete it will return an error 404 - {CATEGORY_NOT_FOUND}.
            """,
        responses={
            204: {"description": CATEGORY_SUCCESSFULLY_DELETED},
            404: {"description": CATEGORY_NOT_FOUND},
        },
    )
    def delete(self, request, _id, *args, **kwargs):

        category = get_category_by_id(_id=_id)
        if not category:
            logger.error(f"The category {_id} doesn't exist!")
            return Response(CATEGORY_NOT_FOUND, status=404)
        category.delete()

        return Response(CATEGORY_SUCCESSFULLY_DELETED, status=204)


class CategoryApiView(APIView):

    @extend_schema(
        methods=["get"],
        description=f"""
            - An endpoint to retrieve some specific category (by ID - record of the category).
            - If non existing category is trying to retrieve it will return an error 404 - {CATEGORY_NOT_FOUND}.
            """,
        responses={
            200: CategorySerializer(many=False),
            404: {"description": CATEGORY_NOT_FOUND},
        },
    )
    def get(self, request, _id, *args, **kwargs):

        category = get_category_by_id(_id=_id)
        if not category:
            logger.error(f"The category {_id} doesn't exist!")
            return Response(data=CATEGORY_NOT_FOUND, status=404)
        response = CategorySerializer(instance=category, many=False).data

        return Response(data=response, status=200)
