from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers, serializers, viewsets

from todos.models import Todo


# Serializers define the API representation.
class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'id',
            'text',
            'priority',
            'complete',
        )


# ViewSets define the view behavior.
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    )
)
