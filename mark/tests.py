import json

from mark.models import Mark
from mark.queries import get_mark_by_id
from pet_shop.error_messages import *
from pet_shop.ok_messages import *
from pet_shop.tests import (
    BaseTestCase,
    client,
)

base_url = "/api/v1"
urls = {
    "all_marks": f"{base_url}/marks/",
    "new_mark": f"{base_url}/marks/new",
    "edit_mark": f"{base_url}/marks/%s/edit",
    "delete_mark": f"{base_url}/marks/%s/delete",
    "get_mark": f"{base_url}/marks/%s",
}


class TestMarkListApiView(BaseTestCase):

    def test_get_pass(self):

        mark = Mark(name="test_mark")
        mark.save()

        response = client.get(path=urls.get("all_marks"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), list)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0].get("name"), mark.name)
        self.assertEqual(content[0].get("id"), mark.id)

    def test_get_not_found(self):

        response = client.get(path=urls.get("all_marks"))
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, MARKS_NOT_FOUND)


class TestNewMarkApiView(BaseTestCase):

    def test_post_pass(self):

        mark = Mark(name="test_mark")
        mark.save()

        response = client.post(
            path=urls.get("new_mark"),
            data=json.dumps({"name": "test_mark_name"}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(content, MARK_SUCCESSFULLY_CREATED)

    def test_post_wrong_data_body_validation(self):

        response = client.post(
            path=urls.get("new_mark"),
            data=json.dumps({"name": True}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_post_wrong_data_duplicate_mark(self):

        mark = Mark(name="test_mark")
        mark.save()

        response = client.post(
            path=urls.get("new_mark"),
            data=json.dumps({"name": mark.name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestEditMarkApiView(BaseTestCase):

    def test_patch_pass(self):

        mark = Mark(name="test_mark")
        mark.save()

        mark_name = mark.name

        new_mark_name = "test_mark_updated"

        response = client.patch(
            path=urls.get("edit_mark") % mark.id,
            data=json.dumps({"name": new_mark_name}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 204)

        updated_mark = get_mark_by_id(_id=mark.id)

        self.assertEqual(updated_mark.id, mark.id)
        self.assertNotEqual(updated_mark.name, mark_name)
        self.assertEqual(updated_mark.name, new_mark_name)

    def test_patch_not_found(self):

        new_name = "test_mark_updated"

        response = client.patch(
            path=urls.get("edit_mark") % 1,
            data=json.dumps({"name": new_name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, MARK_NOT_FOUND)

    def test_patch_wrong_data_body_validation(self):

        mark = Mark(name="test_mark")
        mark.save()

        new_name = True

        response = client.patch(
            path=urls.get("edit_mark") % mark.id,
            data=json.dumps({"name": new_name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)

    def test_patch_wrong_data_duplicate_mark(self):

        mark = Mark(name="test_mark")
        mark.save()

        mark_2 = Mark(name="test_mark_2")
        mark_2.save()

        response = client.patch(
            path=urls.get("edit_mark") % mark.id,
            data=json.dumps({"name": mark_2.name}),
            content_type='application/json',
        )
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, WRONG_DATA)


class TestDeleteMarkApiView(BaseTestCase):

    def test_delete_pass(self):

        mark = Mark(name="test_mark")
        mark.save()

        mark_id = mark.id

        response = client.delete(path=urls.get("delete_mark") % mark.id)

        self.assertEqual(response.status_code, 204)

        mark = get_mark_by_id(_id=mark_id)

        self.assertEqual(mark, None)

    def test_delete_not_found(self):

        response = client.delete(path=urls.get("delete_mark") % 1)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, MARK_NOT_FOUND)


class TestMarkApiView(BaseTestCase):

    def test_get_pass(self):

        mark = Mark(name="test_mark")
        mark.save()

        response = client.get(path=urls.get("get_mark") % mark.id)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), dict)
        self.assertEqual(content.get("name"), mark.name)
        self.assertEqual(content.get("id"), mark.id)

    def test_get_not_found(self):

        response = client.get(path=urls.get("get_mark") % 1)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(content, MARK_NOT_FOUND)
