from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workshops/fast-and-fun-django-oct-2021/", views.workshops, name="workshops"),
]
