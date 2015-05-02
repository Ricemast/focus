from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic

from todos.models import Todo


class IndexView(generic.ListView):
    model = Todo
    template_name = 'todos/index.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.order_by('priority')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['total'] = Todo.objects.count()
        context['completed'] = Todo.objects.filter(complete=True).count()
        return context


class FocusView(generic.DetailView):
    model = Todo
    template_name = 'todos/focus.html'


def complete(request, pk):
    """Redirect view to complete the task and move onto the next one"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.complete = True
    todo.save()
    if todo.next:
        return HttpResponseRedirect(
            reverse('todos:focus', args=(todo.next.pk,))
        )
    return HttpResponseRedirect(reverse('todos:index'))


def reset(request):
    """Make all todos not complete"""
    todos = Todo.objects.all()
    for todo in todos:
        todo.complete = False
        todo.save()
    return HttpResponseRedirect(reverse('todos:index'))
