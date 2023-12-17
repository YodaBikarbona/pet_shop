from unittest import TestCase

from django.db import connections
from django.test import Client

from animal.models import Animal
from category.models import Category
from image.models import Image
from mark.models import Mark

models = [Animal, Category, Mark, Image]
tables = [model._meta.db_table for model in models]

client = Client()


class BaseTestCase(TestCase):

    def setUp(self):
        for model in models:
            model.objects.all().delete()

        with connections['default'].cursor() as cursor:

            for table in tables:
                query = "UPDATE SQLITE_SEQUENCE SET " + f"SEQ=0 WHERE NAME='{table}';"
                cursor.execute(query)

    def tearDown(self):

        for model in models:
            model.objects.all().delete()

        with connections['default'].cursor() as cursor:

            for table in tables:
                query = "UPDATE SQLITE_SEQUENCE SET " + f"SEQ=0 WHERE NAME='{table}';"
                cursor.execute(query)
