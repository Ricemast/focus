from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
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


class ToggleTodoStatusView(generic.detail.SingleObjectMixin, generic.View):
    """
    Swaps the status of a todo. If it is marked as complete, change it to
    incomplete. If marked as incomplete, change to complete.
    """
    model = Todo

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.complete = not self.object.complete
        self.object.save()

        return JsonResponse(
            {
                'pk': self.object.pk,
                'complete': self.object.complete,
                'numcompleted': Todo.objects.filter(complete=True).count()
            }
        )


class CompleteTodoView(generic.detail.SingleObjectMixin, generic.View):
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
