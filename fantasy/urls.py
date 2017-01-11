"""fantasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from league import views
from django.conf.urls.static import static
from fantasy import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('league.urls')),
    url(r'^s3direct/', include('s3direct.urls')),
    # url(r'^login/$', 'social.apps.django_app.login'),
    # url(r'^logout/$', 'social.apps.django_app.logout'),
    # url(r'^email/$', 'social_login.views.require_email', name='require_email'),
    # url(r'^complete/email/$', 'social_login.views.home')
    url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/register/$', 'league.views.register', name='register'),
    url(r'^accounts/register/complete/$', 'league.views.registration_complete', name='registration_complete'),
    # url(r'^accounts/', include('registration.backends.simple.urls')),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login',
    #    {'template_name': 'admin/login.html'}),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)