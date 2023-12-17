from django.urls import path

from category.views import (
    CategoryApiView,
    CategoryListApiView,
    DeleteCategoryApiView,
    EditCategoryApiView,
    NewCategoryApiView,
)

urlpatterns = [
    path('', CategoryListApiView.as_view(), name="all_categories"),
    path('new', NewCategoryApiView.as_view(), name="new_category"),
    path('<int:_id>', CategoryApiView.as_view(), name="get_category"),
    path('<int:_id>/edit', EditCategoryApiView.as_view(), name="edit_category"),
    path('<int:_id>/delete', DeleteCategoryApiView.as_view(), name="delete_category"),
]
