from django.core.urlresolvers import reverse
from django.test import TestCase

from todos.models import Todo


def create_todo(todo_text="test"):
    """
    Creates a new todo with the lowest possible priority.
    """
    p = Todo.objects.count() + 1
    return Todo.objects.create(
        text=todo_text,
        priority=p
    )


class TodoPropTests(TestCase):
    def test_next_prop_with_single_todo(self):
        """
        The next property on Todo should return None if it is the only (last)
        todo object.
        """
        todo = create_todo()

        self.assertIsNone(todo.next)

    def test_next_prop_with_multiple_todos(self):
        """
        The next property on Todo should return the todo object with the next
        highest priority if there is one.
        """
        todo = create_todo()
        todo2 = create_todo('test2')

        self.assertEqual(todo.next, todo2)


class TodoIndexViewTests(TestCase):
    def test_index_view_with_no_todos(self):
        """
        If no todos exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('todos:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks yet.")

    def test_index_view_with_single_todo(self):
        """
        If there is a todo object, it should be displayed.
        """
        todo = create_todo()
        response = self.client.get(reverse('todos:index'))
        self.assertContains(response, todo.text)

    def test_index_view_with_multiple_todos(self):
        """
        If there is are multiple todo object, they should all be displayed.
        """
        todo = create_todo()
        todo2 = create_todo('todo2')
        response = self.client.get(reverse('todos:index'))
        self.assertContains(response, todo.text)
        self.assertContains(response, todo2.text)
