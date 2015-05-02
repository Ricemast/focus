from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views import generic
from django.views.generic.detail import SingleObjectMixin

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


class ToggleTodoStatusView(SingleObjectMixin, generic.View):
    """
    Swaps the status of a todo. If it is marked as complete, change it to
    incomplete. If marked as incomplete, change to complete.
    """
    model = Todo

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.complete = not self.object.complete
        self.object.save()

        return JsonResponse({'complete': self.object.complete})


class CompleteTodoView(SingleObjectMixin, generic.View):
    """Redirect view to complete the task and move onto the next one"""
    model = Todo

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.complete = True
        self.object.save()

        if self.object.next:
            return HttpResponseRedirect(
                reverse('todos:focus', args=(self.object.next.pk,))
            )

        return HttpResponseRedirect(reverse('todos:index'))


def reset(request):
    """Make all todos not complete"""
    todos = Todo.objects.all()
    for todo in todos:
        todo.complete = False
        todo.save()
    return HttpResponseRedirect(reverse('todos:index'))
