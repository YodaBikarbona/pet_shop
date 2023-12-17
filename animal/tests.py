import json

from django.urls import reverse

from animal.models import Animal
from animal.queries import get_animal_by_id
from category.models import Category
from image.models import Image
from mark.models import Mark
from pet_shop.error_messages import *
from pet_shop.ok_messages import *
from pet_shop.tests import (
    BaseTestCase,
    client,
)


class TestAnimalListApiView(BaseTestCase):

    def test_get_pass(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
            image=image
        )
        animal.save()

        response = client.get(path=reverse("all_animals"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), list)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get("animal_id"), animal.animal_id)
        self.assertEqual(content[0].get("name"), animal.name)
        self.assertEqual(content[0].get("id"), animal.id)
        self.assertEqual(content[0].get("status"), animal.status)
        self.assertEqual(content[0].get("category", {}).get("id"), category.id)
        self.assertEqual(content[0].get("mark", {}).get("id"), mark.id)
        self.assertEqual(content[0].get("image", {}).get("id"), image.id)

    def test_get_not_found(self):

        response = client.get(path=reverse("all_animals"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, ANIMALS_NOT_FOUND)


class TestNewAnimalApiView(BaseTestCase):

    def test_post_pass(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        response = client.post(
            path=reverse("new_animal"),
            data=json.dumps({
                "name": "test_animal_name",
                "animal_id": 5720385832,
                "status": "set",
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, ANIMAL_SUCCESSFULLY_CREATED)

    def test_post_wrong_data_body_validation(self):

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        response = client.post(
            path=reverse("new_animal"),
            data=json.dumps({
                "name": "test_animal_name",
                "animal_id": 5720385832,
                "status": "set",
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_category_not_found(self):

        mark = Mark(name="test_mark")
        mark.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        response = client.post(
            path=reverse("new_animal"),
            data=json.dumps({
                "name": "test_animal_name",
                "animal_id": 5720385832,
                "status": "set",
                "category_id": 1,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_mark_not_found(self):

        category = Category(name="test_category")
        category.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        response = client.post(
            path=reverse("new_animal"),
            data=json.dumps({
                "name": "test_animal_name",
                "animal_id": 5720385832,
                "status": "set",
                "category_id": category.id,
                "mark_id": 1,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_invalid_status(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        response = client.post(
            path=reverse("new_animal"),
            data=json.dumps({
                "name": "test_animal_name",
                "animal_id": 5720385832,
                "status": "some_status",
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_duplicate_animal_id(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
            image=image
        )
        animal.save()

        response = client.post(
            path=reverse("new_animal"),
            data=json.dumps({
                "name": "test_animal_name",
                "animal_id": 5720385832,
                "status": "set",
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestEditAnimalApiView(BaseTestCase):

    def test_patch_pass(self):

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

        new_status = "approved"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': animal.id}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal.animal_id,
                "status": new_status,
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 204)

        updated_animal = get_animal_by_id(_id=animal.id)

        self.assertEqual(updated_animal.animal_id, animal.animal_id)
        self.assertEqual(updated_animal.name, animal.name)
        self.assertEqual(updated_animal.id, animal.id)
        self.assertNotEqual(updated_animal.status, animal.status)
        self.assertEqual(updated_animal.status, new_status)
        self.assertEqual(updated_animal.category, category)
        self.assertEqual(updated_animal.mark, mark)

    def test_patch_not_found(self):

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

        new_status = "approved"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': 2}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal.animal_id,
                "status": new_status,
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, ANIMAL_NOT_FOUND)

    def test_patch_wrong_data_body_validation(self):

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

        new_status = "approved"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': animal.id}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal.animal_id,
                "status": new_status,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_patch_wrong_data_category_not_found(self):

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

        new_status = "approved"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': animal.id}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal.animal_id,
                "status": new_status,
                "category_id": 2,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_patch_wrong_data_mark_not_found(self):

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

        new_status = "approved"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': animal.id}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal.animal_id,
                "status": new_status,
                "category_id": category.id,
                "mark_id": 2,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_patch_wrong_data_invalid_status(self):

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

        new_status = "invalid_status"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': animal.id}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal.animal_id,
                "status": new_status,
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_patch_wrong_data_duplicate_animal_id(self):

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

        animal_2 = Animal(
            name="test_animal_name",
            animal_id=5720385833,
            status="set",
            category=category,
            mark=mark,
        )
        animal_2.save()

        new_status = "approved"

        response = client.patch(
            path=reverse("edit_animal", kwargs={'_id': animal.id}),
            data=json.dumps({
                "name": animal.name,
                "animal_id": animal_2.animal_id,
                "status": new_status,
                "category_id": category.id,
                "mark_id": mark.id,
            }),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestDeleteAnimalApiView(BaseTestCase):

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

        animal_id = animal.id

        response = client.delete(
            path=reverse("delete_animal", kwargs={'_id': animal.id}),
        )

        self.assertEqual(response.status_code, 204)

        animal = get_animal_by_id(_id=animal_id)

        self.assertEqual(animal, None)

    def test_delete_not_found(self):

        response=client.delete(path=reverse("delete_animal", kwargs={'_id': 1}))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, ANIMAL_NOT_FOUND)


class TestAnimalApiView(BaseTestCase):

    def test_get_pass(self):

        category = Category(name="test_category")
        category.save()

        mark = Mark(name="test_mark")
        mark.save()

        image = Image(
            name="test_image",
            path="test_image.jpg",
            format="jpg",
        )
        image.save()

        animal = Animal(
            name="test_animal_name",
            animal_id=5720385832,
            status="set",
            category=category,
            mark=mark,
            image=image,
        )
        animal.save()

        response = client.get(path=reverse("get_animal", kwargs={'_id': animal.id}))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), dict)
        self.assertEqual(content.get("animal_id"), animal.animal_id)
        self.assertEqual(content.get("name"), animal.name)
        self.assertEqual(content.get("id"), animal.id)
        self.assertEqual(content.get("status"), animal.status)
        self.assertEqual(content.get("category", {}).get("id"), category.id)
        self.assertEqual(content.get("mark", {}).get("id"), mark.id)
        self.assertEqual(content.get("image", {}).get("id"), image.id)

    def test_get_not_found(self):

        response = client.get(path=reverse("get_animal", kwargs={'_id': 1}))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, ANIMAL_NOT_FOUND)
