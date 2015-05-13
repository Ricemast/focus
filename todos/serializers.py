from rest_framework import serializers

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
