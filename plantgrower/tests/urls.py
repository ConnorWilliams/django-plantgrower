from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^plantgrower/', include('plantgrower.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
