from rest_framework import serializers
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)

from todos.models import Todo


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'id',
            'text',
            'priority',
            'complete',
            'next',
        )


class TodoBulkSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = Todo
        list_serializer_class = BulkListSerializer
