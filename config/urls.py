import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path("", include("denig.urls")),
    path("admin/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("essays/", include(wagtail_urls)),
    path("accounts/", include("authuser.urls")),
    path("prose/", include("prose.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
