from django.urls import path

from image.views import (
    NewImageApiView,
    DeleteImageApiView,
)

urlpatterns = [
    path('new', NewImageApiView.as_view(), name="new_image"),
    path('<int:_id>/delete', DeleteImageApiView.as_view(), name="delete_image"),
]
