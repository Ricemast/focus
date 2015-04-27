from django.conf.urls import url

from todos import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.FocusView.as_view(), name='focus'),
]
