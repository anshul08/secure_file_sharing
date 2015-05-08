from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^download$', views.get_file),
    url(r'^$', views.index),
]