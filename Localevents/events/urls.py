from django.urls import path
from .views import (
    event_list, event_detail,
    event_create, event_edit, event_delete
)

urlpatterns = [
    path("", event_list, name="event_list"),
    path("events/create/", event_create, name="event_create"),
    path("events/<int:pk>/", event_detail, name="event_detail"),
    path("events/<int:pk>/edit/", event_edit, name="event_edit"),
    path("events/<int:pk>/delete/", event_delete, name="event_delete"),
]
