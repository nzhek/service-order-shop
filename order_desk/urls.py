from django.contrib import admin

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', include('public.urls')),
    path('api-v0/', include('api_v0.urls')),
    path('admin/', admin.site.urls),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
