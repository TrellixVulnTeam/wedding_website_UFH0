"""text_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^base/$', views.base),
	url(r'^home/$', views.home, name='home'),
	url(r'^about/$', views.about, name='about'),
	url(r'^weddinginfo/$', views.wedding_info, name='wedding_info'),
	url(r'^rsvp/$', views.rsvp, name='rsvp'),
	url(r'^registry/$', views.registry, name='registry'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^rsvp-thanks/$', views.rsvp_thanks, name='rsvp-thanks'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

