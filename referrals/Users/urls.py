from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'Users/user_logout.html'}, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'Users/user_login.html'}, name='login'),
    url(r'^profile/$', views.user_profile,  name='user_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^activate/([0-9]+)/([0-9]+)$', views.user_activate, name='activate'),
    url(r'^generate$', views.generate_code, name='generate_code'),
    url(r'^top/$', views.top_ten, name='top_ten'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
