from django.views import generic

from todos.models import Todo


class IndexView(generic.ListView):
    model = Todo
    template_name = 'todos/index.html'
    context_object_name = 'todos'


class FocusView(generic.DetailView):
    model = Todo
    template_name = 'todos/focus.html'

    def get_context_data(self, **kwargs):
        """Add the next highest priority todo to the context data"""
        context = super(FocusView, self).get_context_data(**kwargs)
        context['next'] = Todo.objects.order_by('priority').filter(
            priority__gt=self.object.priority
        ).first()
        return context
