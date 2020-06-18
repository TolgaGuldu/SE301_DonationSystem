"""DonSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from DonApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url('', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'regist/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'regist/logged_out.html'}, name='logout'),
    url(r'^campaigns/(?P<pk>\d+)/money_donation/$', views.money_donation, name='money_donation'),
    url(r'^campaigns/(?P<pk>\d+)/item_donation/$', views.item_donation, name='item_donation'),
    url(r'^campaigns/(?P<pk>\d+)/$', views.view_campaign_detail, name='view_campaign_detail'),
    url(r'^campaigns/', views.view_campaigns, name='view_campaigns'),
    url(r'^ngos/(?P<pk>\d+)/money_donation/$', views.ngo_money_donation, name='ngo_money_donation'),
    url(r'^ngos/(?P<pk>\d+)/$', views.view_ngo_detail, name='view_ngo_detail'),
    url(r'^ngos/$', views.view_ngos, name='view_ngos'),
    url(r'^register/asDonator/$', views.registerDonator, name='registerDonator'),
    url(r'^register/asNGO/$', views.registerNGO, name='registerNGO'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/received_donations/$', views.view_received_donations, name='view_received_donations'),
    url(r'^profile/edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/my_donations/$', views.view_my_donations, name='view_my_donations'),
    url(r'^profile/campaigns/create_campaign/$', views.create_campaign, name='create_campaign'),
    url(r'^profile/campaigns/edit_campaign/$', views.edit_my_campaign, name='edit_my_campaign'),
    url(r'^profile/campaigns/$', views.my_campaigns, name='my_campaigns'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
]


