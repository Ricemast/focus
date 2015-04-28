from django.conf.urls import url

from todos import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.FocusView.as_view(), name='focus'),
    url(
        r'^(?P<pk>[0-9]+)/complete/$',
        views.complete,
        name='complete',
    ),
    url(
        r'^reset/$',
        views.reset,
        name='reset',
    ),
]
