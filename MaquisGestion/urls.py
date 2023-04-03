#import concernant les image

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Stock.urls')),
    path('compte/', include('compte.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)


handler404="Stock.views.error404"