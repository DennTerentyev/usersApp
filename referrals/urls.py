from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from Users import urls as users_urls
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include(users_urls)),
    url(r'^accounts/profile', RedirectView.as_view(url='/users/profile/')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
