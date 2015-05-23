from rest_framework import generics
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from todos.models import Todo
from todos.serializers import TodoSerializer, TodoBulkSerializer


class TodoList(ListBulkCreateUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoBulkSerializer

    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        # restrict the update to the filtered queryset
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_update(serializer)

        serializer = self.serializer_class(Todo.objects.all(), many=True)
        return Response(serializer.data)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        serializer = self.serializer_class(Todo.objects.all(), many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        for todo in Todo.objects.filter(priority__gt=instance.priority):
            todo.priority -= 1
            todo.save()

        serializer = self.serializer_class(Todo.objects.all(), many=True)
        return Response(serializer.data)
