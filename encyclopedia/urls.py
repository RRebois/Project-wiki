from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:word>", views.query, name="query"),
    path("wiki/", views.search, name="search"),
    path("wiki/newPage/", views.newPage, name="newPage"),
    path("wiki/editpage/", views.editPage, name="editPage"),
    path("wiki/saveEdit/", views.saveEdit, name="saveEdit"),
]
