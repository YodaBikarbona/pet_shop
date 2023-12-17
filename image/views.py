import logging
import os

from PIL import Image as PilImage
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from animal.queries import get_animal_by_id
from image.helper import remove_image
from image.models import Image
from image.queries import get_image_by_id
from image.serializers import NewImageSerializer
from pet_shop import settings
from pet_shop.error_messages import *
from pet_shop.ok_messages import *
from pet_shop.settings import (
    DEFAULT_MEDIA_URL,
    MAX_IMAGE_SIZE,
)

logger = logging.getLogger(__name__)


class NewImageApiView(APIView):

    @extend_schema(
        methods=["post"],
        description=f"""
            - An endpoint to create new image for some animal.
            - If one of the body data is wrong it will return an error 400 - {WRONG_DATA}
            - Adding new image on some animal that has the image, old image will be deleted and new will be created.
            - To use binary field (button) change the body from application/json to multipart/form-data
            """,
        request=NewImageSerializer(many=False),
        responses={
            201: {"description": IMAGE_SUCCESSFULLY_CREATED},
            400: {"description": WRONG_DATA},
        },
    )
    @parser_classes([MultiPartParser])
    def post(self, request, *args, **kwargs):

        data = NewImageSerializer(data=request.data)
        if not data.is_valid():
            logger.error("The data is wrong!")
            return Response(WRONG_DATA, status=400)

        animal = get_animal_by_id(_id=data.validated_data.get("id"))
        if not animal:
            logger.error(f"The animal {data.validated_data.get("id")} doesn't exist!")
            return Response(WRONG_DATA, status=400)

        size_in_mb = data.validated_data.get("image").size / (1024 * 1024)
        if size_in_mb > MAX_IMAGE_SIZE:
            logger.error(f"The image has the size: {size_in_mb} higher than maximum size!")
            return Response(WRONG_DATA, status=400)
        file_name = get_random_string(length=64)
        try:
            image = PilImage.open(data.validated_data.get("image"))
            image_format = image.format.lower()
            file_path = os.path.join(settings.MEDIA_ROOT, f"{file_name}.{image_format}")
            image.save(file_path)
            path = f"{DEFAULT_MEDIA_URL}{file_name}.{image_format}"
            new_image = Image(
                name=file_name,
                path=path,
                format=image_format,
            )
            new_image.save()
        except Exception as ex:
            logger.error(f"The image cannot be saved! ex:{ex}")
            return Response(WRONG_DATA, status=400)

        if animal.image:
            if remove_image(path=f"{animal.image.name}.{animal.image.format}"):
                animal.image.delete()
        animal.image = new_image
        animal.save()

        return Response(IMAGE_SUCCESSFULLY_CREATED, status=201)


class DeleteImageApiView(APIView):

    @extend_schema(
        methods=["delete"],
        description=f"""
            - An endpoint to delete existing image (by ID - record of the image).
            - If non existing image is trying to delete it will return an error 404 - {IMAGE_NOT_FOUND}.
            """,
        responses={
            204: {"description": IMAGE_SUCCESSFULLY_DELETED},
            404: {"description": IMAGE_NOT_FOUND},
        },
    )
    def delete(self, request, _id, *args, **kwargs):

        image = get_image_by_id(_id=_id)
        if not image:
            logger.error(f"The image {_id} doesn't exist!")
            return Response(data=IMAGE_NOT_FOUND, status=404)
        if not remove_image(path=f"{image.name}.{image.format}"):
            return Response(WRONG_DATA, status=400)
        image.delete()

        return Response(IMAGE_SUCCESSFULLY_DELETED, status=204)
