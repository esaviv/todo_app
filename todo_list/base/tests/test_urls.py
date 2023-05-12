from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus

from ..models import Task

User = get_user_model()

class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username="auth")
        cls.task = Task.objects.create(
            user=cls.auth,
            title="Тестовое задание",
            description="Тестовое описание",
        )

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(self.auth)

        self.guest_client = Client()


    def test_urls_exist_at_desired_location_anonymous(self):
        urls = [
            "/register/",
            "/login/",
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirect_anonymous_on_admin_login(self):
        login_first = "/login/?next="
        urls = {
            "/logout/": "/login/",
            "/": f"{login_first}/",
            f"/task/{self.task.pk}/": f"{login_first}/task/{self.task.pk}/",
            "/create/": f"{login_first}/create/",
            f"/task/{self.task.pk}/update/": f"{login_first}/task/{self.task.pk}/update/",
            f"/task/{self.task.pk}/delete/": f"{login_first}/task/{self.task.pk}/delete/"
        }
        for url, redirect_url in urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_urls_use_correct_template_anonymous(self):
        url_template_names = {
            # "/logout/": "base/",
            "/register/": "base/register.html",
            "/login/": "base/login.html",
            # "/": "base/task_list.html",
            # f"/task/{self.task.pk}/": "base/task.html",
            # "/create/": "base/task_form.html",
            # f"/task/{self.task.pk}/update/": "base/",
            # f"/task/{self.task.pk}/delete/": "base/task_confirm_delete.html"
        }
        for url, template in url_template_names.items():
            with self.subTest(url=url, template=template):
                response = self.authorized_author.get(url)
                self.assertTemplateUsed(response, template)


