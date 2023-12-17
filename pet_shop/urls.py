from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularRedocView,
    SpectacularAPIView,
)

from pet_shop import settings
from pet_shop.settings import BASE_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path(BASE_URL, include(
        [
            path('categories/', include('category.urls'), name="categories"),
            path('marks/', include('mark.urls'), name="marks"),
            path('animals/', include('animal.urls'), name="animals"),
            path('images/', include('image.urls'), name="images"),
        ]
    )),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/doc', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
