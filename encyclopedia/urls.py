from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new_entry", views.new, name="new_entry"),
    path("random", views.random, name="random_page"),
    path("edit_entry/<str:name>", views.edit, name="edit_entry"),
    path("<str:name>", views.dynamic, name="dynamic")
]
