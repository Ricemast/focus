from django.conf.urls import patterns, include, url
from django.contrib import admin

from todos.api import TodoResource

todo_resource = TodoResource()

urlpatterns = patterns(
    '',

    url(r'^', include('todos.urls', namespace='todos')),
    url(r'^api/', include(todo_resource.urls)),

    url(r'^admin/', include(admin.site.urls)),
)
