from django.http import JsonResponse
from django.views import generic

from rest_framework import generics

from todos.models import Todo
from todos.serializers import TodoSerializer


class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class ResetAllTodosView(generic.list.MultipleObjectMixin, generic.View):
    """Make all todos not complete"""
    model = Todo

    def post(self, request, *args, **kwargs):
        self.queryset = self.get_queryset()
        for todo in self.queryset:
            todo.complete = False
            todo.save()

        return JsonResponse(
            {
                'reset': True,
                'numcompleted': Todo.objects.filter(complete=True).count()
            }
        )


class ReorderTodosView(generic.View):
    """Reorder the todo objects according to changes envoked in UI."""

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.iteritems():
            if key != 'csrfmiddlewaretoken':
                todo = Todo.objects.get(pk=key)
                todo.priority = value
                todo.save()

        return JsonResponse({'reordered': True})
