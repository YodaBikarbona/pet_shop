from django.urls import path

from animal.views import (
    AnimalApiView,
    AnimalListApiView,
    NewAnimalApiView,
    EditAnimalApiView,
    DeleteAnimalApiView,
)

urlpatterns = [
    path('', AnimalListApiView.as_view(), name="all_animals"),
    path('<int:_id>', AnimalApiView.as_view(), name="get_animal"),
    path('new', NewAnimalApiView.as_view(), name="new_animal"),
    path('<int:_id>/edit', EditAnimalApiView.as_view(), name="edit_animal"),
    path('<int:_id>/delete', DeleteAnimalApiView.as_view(), name="delete_animal"),
]
