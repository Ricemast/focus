from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from todos.models import Todo
from todos.serializers import TodoSerializer, TodoBulkSerializer


class TodoList(ListBulkCreateUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoBulkSerializer


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print instance
        self.perform_destroy(instance)
        for todo in Todo.objects.filter(priority__gt=instance.priority):
            todo.priority -= 1
            todo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
