from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ALIREZA — Studio Control"
admin.site.site_title = "ALIREZA Admin"
admin.site.index_title = "Portfolio & inquiries"

urlpatterns = [
    path("studio-control/", admin.site.urls),
    path("", include("portfolio.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
