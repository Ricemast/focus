from rest_framework import generics
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from todos.models import Todo
from todos.serializers import TodoSerializer, TodoBulkSerializer


class TodoList(ListBulkCreateUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoBulkSerializer


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
