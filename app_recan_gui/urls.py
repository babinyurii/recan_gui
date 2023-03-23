from django.urls import path
from . import views


urlpatterns = [
    path("", views.recan_view, name="recan_view"),
]
