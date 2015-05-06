from django.conf.urls import url

from todos import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.FocusView.as_view(), name='focus'),
    url(
        r'^(?P<pk>[0-9]+)/toggle/$',
        views.ToggleTodoStatusView.as_view(),
        name='toggle'
    ),
    url(
        r'^(?P<pk>[0-9]+)/complete/$',
        views.CompleteTodoView.as_view(),
        name='complete',
    ),
    url(
        r'^reset/$',
        views.ResetAllTodosView.as_view(),
        name='reset',
    ),
    url(
        r'^reorder/$',
        views.ReorderTodosView.as_view(),
        name='reorder',
    ),
]
