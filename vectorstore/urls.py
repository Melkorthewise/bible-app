# vectorstore/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search_view, name="vector-search"),
    path("your-name/", views.get_name, name="name"),
]

