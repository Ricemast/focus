from django.http import JsonResponse
from django.views import generic

from rest_framework import generics
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from todos.models import Todo
from todos.serializers import TodoSerializer, TodoBulkSerializer


class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoReset(ListBulkCreateUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoBulkSerializer


class ReorderTodosView(generic.View):
    """Reorder the todo objects according to changes envoked in UI."""

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.iteritems():
            if key != 'csrfmiddlewaretoken':
                todo = Todo.objects.get(pk=key)
                todo.priority = value
                todo.save()

        return JsonResponse({'reordered': True})
