from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Task

User = get_user_model()


class TaskModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username="auth")
        cls.task = Task.objects.create(
            user=cls.auth,
            title="Тестовое задание",
            description="Тестовое описание",
        )

    def test_model_has_correct_object_name(self):
        task = TaskModelTests.task
        self.assertEqual(task.title, str(task))

    def test_verbose_name(self):
        task = TaskModelTests.task
        field_verboses = {
            "title": "Название",
            "description": "Описание",
            "complete": "Выполнено?",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value
                )

    def test_model_has_correct_ordering(self):
        task = TaskModelTests.task
        self.assertEqual(task._meta.ordering, ["complete"])
