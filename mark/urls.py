from django.urls import path

from mark.views import (
    MarkApiView,
    DeleteMarkApiView,
    EditMarkApiView,
    NewMarkApiView,
    MarkListApiView,
)


urlpatterns = [
    path('', MarkListApiView.as_view(), name="all_marks"),
    path('new', NewMarkApiView.as_view(), name="new_mark"),
    path('<int:_id>', MarkApiView.as_view(), name="get_mark"),
    path('<int:_id>/edit', EditMarkApiView.as_view(), name="edit_mark"),
    path('<int:_id>/delete', DeleteMarkApiView.as_view(), name="delete_mark"),
]
