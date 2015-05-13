from django.conf.urls import url

from todos import views

urlpatterns = [
    url(r'^$', views.TodoList.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.TodoDetail.as_view(), name='focus'),

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
    url(
        r'^add/$',
        views.CreateTodoView.as_view(),
        name='create',
    )
]
