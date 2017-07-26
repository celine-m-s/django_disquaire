from django.conf.urls import url

from . import views

app_name = 'store'


urlpatterns = [
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^$', views.listing, name='listing')
]
