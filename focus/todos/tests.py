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


class TodoMethodTests(TestCase):
    def test_creating_a_todo_with_no_fields_creates_a_new_todo(self):
        """
        Creating a new todo without any fields should create a new todo with
        the test 'New Todo'.
        """
        todo = Todo.objects.create()

        self.assertEqual(todo.text, 'New Todo')

    def test_creating_a_todo_with_all_the_fields(self):
        """
        Creating a new todo and provided all of the fields should work.
        """
        Todo.objects.create(
            text='test',
            priority=10,
            complete=True
        )

        todo = Todo.objects.get(text='test')
        self.assertEqual(todo.priority, 10)
        self.assertEqual(todo.complete, True)

    def test_creating_a_todo_with_only_the_required_fields(self):
        """
        Creating a new todo and providing only the required fields should work.
        """
        Todo.objects.create(
            text='test'
        )

        count = Todo.objects.count()

        todo = Todo.objects.get(text='test')
        self.assertEqual(todo.priority, count)

    def test_creating_todo_without_priority_adds_to_end_of_list(self):
        """
        Creating a new todo without assigning a priority should add it
        to the end of the list.
        """
        todo = Todo.objects.create(text='test')
        last = Todo.objects.all().last()
        count = Todo.objects.count()

        self.assertEqual(todo, last)
        self.assertEqual(todo.priority, count)

    def test_creating_todo_with_existing_priority_pushes_the_list(self):
        """
        When creating a todo with a priority that already exists, the objects
        with a priority gte should be pushed down
        """
        old_priority1 = Todo.objects.create(
            text='test',
            priority=1
        )

        new_priority1 = Todo.objects.create(
            text='new_priorty_one',
            priority=1
        )

        self.assertEqual(Todo.objects.get(priority=1), new_priority1)
        self.assertEqual(Todo.objects.get(priority=2), old_priority1)


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

    def test_index_view_clicking_on_a_todo(self):
        """
        Clicking on a todo in the view should direct you to the focus
        view for that object.
        """
        todo = Todo.objects.create(text='test')
        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, todo.text)


class TodoResetViewTests(TestCase):
    def test_reset_view_makes_all_of_the_todos_complete_eq_false(self):
        """
        When navigating to the reset view, all todo objects should be
        marked as incomplete.
        """
        Todo.objects.create(text='complete', complete=True)

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            1
        )

        self.client.get(reverse('todos:reset'))

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            0
        )

    def test_reset_view_redirects_to_index_view_with_todos(self):
        """
        After the reset view's logic has been completed, the client
        should be redirected to the index view.
        """
        Todo.objects.create(text='complete', complete=True)

        response = self.client.get(reverse('todos:reset'))

        self.assertRedirects(
            response,
            reverse('todos:index')
        )

    def test_reset_view_redirects_to_index_view_without_todos(self):
        """
        If navigation to the reset view when there are no todo objects,
        the client should be redirected to the index view without error.
        """
        self.assertEqual(Todo.objects.count(), 0)

        response = self.client.get(reverse('todos:reset'))

        self.assertRedirects(
            response,
            reverse('todos:index')
        )
