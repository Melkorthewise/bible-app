# vectorstore/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search_view, name="vector-search"),
]

