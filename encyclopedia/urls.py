from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:word>", views.query, name="query"),
    path("wiki/", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
]
