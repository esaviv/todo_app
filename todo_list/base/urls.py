from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (TaskList,
                    TaskDetail,
                    TaskCreate,
                    TaskUpdate,
                    TaskDelete,
                    CustomLoginView,
                    RegisterPage)

app_name = "base"

urlpatterns = [
    path("register/", RegisterPage.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="base:login"), name="logout"),
    path("", TaskList.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("create/", TaskCreate.as_view(), name="create"),
    path("task/<int:pk>/update/", TaskUpdate.as_view(), name="update"),
    path("task/<int:pk>/delete/", TaskDelete.as_view(), name="delete"),
]
