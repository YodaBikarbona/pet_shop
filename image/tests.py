import json
import os.path

from django.core.files.uploadedfile import SimpleUploadedFile

from animal.models import Animal
from animal.queries import get_animal_by_id
from category.models import Category
from image.queries import get_image_by_id
from mark.models import Mark
from pet_shop.error_messages import *
from pet_shop.ok_messages import *
from pet_shop.tests import (
    BaseTestCase,
    client,
)

base_url = "/api/v1"
urls = {
    "new_image": f"{base_url}/images/new",
    "delete_image": f"{base_url}/images/%s/delete",
}


class TestNewImageApiView(BaseTestCase):

    def test_post_pass(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        self.assertEqual(animal.image, None)

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, IMAGE_SUCCESSFULLY_CREATED)

        animal = get_animal_by_id(_id=animal.id)

        self.assertNotEqual(animal.image, None)
        self.assertEqual(animal.image.id, 1)

    def test_post_pass_overwrite_old_image(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        self.assertEqual(animal.image, None)

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, IMAGE_SUCCESSFULLY_CREATED)

        animal = get_animal_by_id(_id=animal.id)

        old_animal_image_id = animal.image.id

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image_2.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, IMAGE_SUCCESSFULLY_CREATED)

        image = get_image_by_id(_id=old_animal_image_id)
        animal = get_animal_by_id(_id=animal.id)

        self.assertNotEqual(animal.image, None)
        self.assertEqual(image, None)
        self.assertNotEqual(animal.image.id, old_animal_image_id)
        self.assertEqual(animal.image.id, 2)

    def test_post_wrong_data_body_validation(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_animal_not_found(self):

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": 1,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_to_big_image(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        self.assertEqual(animal.image, None)

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image_5_mb.jpg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_invalid_format(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        self.assertEqual(animal.image, None)

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image_invalid_format.png")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestDeleteImageApiView(BaseTestCase):

    def test_delete_pass(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        self.assertEqual(animal.image, None)

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, IMAGE_SUCCESSFULLY_CREATED)

        animal = get_animal_by_id(_id=animal.id)

        self.assertNotEqual(animal.image, None)
        self.assertEqual(animal.image.id, 1)

        response = client.delete(path=urls.get("delete_image") % animal.image.id)

        self.assertEqual(response.status_code, 204)

    def test_delete_not_found(self):

        response = client.delete(path=urls.get("delete_image") % 1)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, IMAGE_NOT_FOUND)

    def test_delete_wrong_data_the_image_file_not_found(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
        )
        animal.save()

        self.assertEqual(animal.image, None)

        image_path = os.path.join(os.path.dirname(__file__), "tests_media", "test_image.jpeg")

        with open(image_path, "rb") as _image:
            image = _image.read()

        data = {
            "image": SimpleUploadedFile("test_image.jpeg", image, content_type="image/jpeg"),
            "id": animal.id,
        }

        response = client.post(
            path=urls.get("new_image"),
            data=data,
            format="multipart",
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, IMAGE_SUCCESSFULLY_CREATED)

        animal = get_animal_by_id(_id=animal.id)

        self.assertNotEqual(animal.image, None)
        self.assertEqual(animal.image.id, 1)

        image = animal.image
        image.name = "invalid_image_file"
        image.save()

        response = client.delete(path=urls.get("delete_image") % animal.image.id)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)
