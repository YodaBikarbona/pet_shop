import json

from django.urls import reverse

from category.models import Category
from category.queries import get_category_by_id
from pet_shop.error_messages import *
from pet_shop.ok_messages import *
from pet_shop.tests import (
    BaseTestCase,
    client,
)


class TestCategoryListApiView(BaseTestCase):

    def test_get_pass(self):

        category = Category(name="test_category")
        category.save()

        response = client.get(path=reverse("all_categories"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), list)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get("name"), category.name)
        self.assertEqual(content[0].get("id"), category.id)

    def test_get_not_found(self):

        response = client.get(path=reverse("all_categories"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, CATEGORIES_NOT_FOUND)


class TestNewCategoryApiView(BaseTestCase):

    def test_post_pass(self):

        response = client.post(
            path=reverse("new_category"),
            data=json.dumps({"name": "test_category_name"}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, CATEGORY_SUCCESSFULLY_CREATED)

    def test_post_wrong_data_body_validation(self):

        response = client.post(
            path=reverse("new_category"),
            data=json.dumps({"name": True}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_duplicate_category(self):

        category = Category(name="test_category")
        category.save()

        response = client.post(
            path=reverse("new_category"),
            data=json.dumps({"name": category.name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestEditCategoryApiView(BaseTestCase):

    def test_patch_pass(self):

        category = Category(name="test_category")
        category.save()

        new_name = "test_category_updated"

        response = client.patch(
            path=reverse("edit_category", kwargs={'_id': category.id}),
            data=json.dumps({"name": new_name}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 204)

        updated_category = get_category_by_id(_id=category.id)

        self.assertEqual(updated_category.name, new_name)
        self.assertEqual(updated_category.id, category.id)
        self.assertNotEqual(updated_category.name, category.name)

    def test_patch_not_found(self):

        new_name = "test_category_updated"

        response = client.patch(
            path=reverse("edit_category", kwargs={'_id': 2}),
            data=json.dumps({"name": new_name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, CATEGORY_NOT_FOUND)

    def test_patch_wrong_data_body_validation(self):

        category = Category(name="test_category")
        category.save()

        response = client.patch(
            path=reverse("edit_category", kwargs={'_id': category.id}),
            data=json.dumps({"name": True}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_patch_wrong_data_duplicate_category(self):

        category = Category(name="test_category")
        category.save()

        category_2 = Category(name="test_category_2")
        category_2.save()

        response = client.patch(
            path=reverse("edit_category", kwargs={'_id': category.id}),
            data=json.dumps({"name": category_2.name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestDeleteCategoryApiView(BaseTestCase):

    def test_delete_pass(self):

        category = Category(name="test_category")
        category.save()

        category_id = category.id


        response = client.delete(
            path=reverse("delete_category", kwargs={'_id': category.id}),
        )

        self.assertEqual(response.status_code, 204)

        category = get_category_by_id(_id=category_id)

        self.assertEqual(category, None)

    def test_delete_not_found(self):

        response = client.delete(path=reverse("delete_category", kwargs={'_id': 1}))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, CATEGORY_NOT_FOUND)


class TestCategoryApiView(BaseTestCase):

    def test_get_pass(self):

        category = Category(name="test_category")
        category.save()

        response = client.get(
            path=reverse("get_category", kwargs={'_id': category.id}),
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), dict)
        self.assertEqual(content.get("name"), category.name)
        self.assertEqual(content.get("id"), category.id)

    def test_get_not_found(self):

        response = client.get(path=reverse("get_category", kwargs={'_id': 1}))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, CATEGORY_NOT_FOUND)
