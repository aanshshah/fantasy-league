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
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
urlpatterns = [
url(r'^$', views.about),
url('login', 'django.contrib.auth.views.login'),
# url('login', 'django.contrib.auth.views.login'),
    url('logout', views.logout_page),
    url('accounts/login/', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    # url(r'^accounts/', include('registration.backends.simple.urls')),
    # url('register', views.register),
    # url('success', views.register_success),
url('request_trade', views.request_trade),
    url('home', views.home),
    url('profile', views.profile),
    url('delete_player',views.delete_player),
    url('add_player', views.add_player),
    url('profile/add_player', views.add_player),
    url('rater', views.make_rater),
    url('create_rating', views.rater_page),
    url('modify_rating', views.modify_rating),
    url('trade', views.trade_page),
    url('404', views.test_404),
    # url('delete_player', views.delete_player),
    url('profile/delete_player', views.delete_player),
    url('create_league', views.create_league),
    url('search_league', views.search_league),
    url('search_player', views.search_player),
    url('join_league', views.join_league),
    url('admin', views.admin_page),
    url(r'league/(?P<league_id>[0-9]+)$', views.get_league_page),
    url('league', views.league),
    url('create_pairings', views.create_pairings),
    url('calculate_winner', views.calculate_winner),
    url('recent', views.recent_page),
    # Registration URLs
    url(r'^accounts/register/$', 'league.views.register', name='register'),
    url(r'^accounts/register/complete/$', 'league.views.registration_complete', name='registration_complete'),
]
# urlpatterns += staticfiles_urlpatterns()