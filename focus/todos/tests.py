import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from todos.models import Todo


class TodoPropTests(TestCase):
    def test_next_prop_with_single_todo(self):
        """
        The next property on Todo should return None if it is the only (last)
        todo object.
        """
        todo = Todo.objects.create(text='test')

        self.assertIsNone(todo.next)

    def test_next_prop_with_multiple_todos(self):
        """
        The next property on Todo should return the todo object with the next
        highest priority if there is one.
        """
        todo = Todo.objects.create(text='test')
        todo2 = Todo.objects.create(text='test2')

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
        last = Todo.objects.last()
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

    def test_create_a_todo_with_no_priority_and_gaps_in_priorities(self):
        """
        Bug #8: A todo will be created with the priority eq to the lowest
        available priority. This should not be the case. It should be created
        with priority higher than all other todos. i.e. the end of the list.
        """
        Todo.objects.create(text='test', priority=2)
        todo = Todo.objects.create(text='priority3')

        self.assertEqual(todo.priority, 3)


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
        todo = Todo.objects.create(text='test')
        response = self.client.get(reverse('todos:index'))
        self.assertContains(response, todo.text)

    def test_index_view_with_multiple_todos(self):
        """
        If there is are multiple todo object, they should all be displayed.
        """
        todo = Todo.objects.create(text='test')
        todo2 = Todo.objects.create(text='test2')
        response = self.client.get(reverse('todos:index'))
        self.assertContains(response, todo.text)
        self.assertContains(response, todo2.text)

    def test_index_view_clicking_on_a_todo_takes_to_focus_view(self):
        """
        Clicking on a todo in the view should direct you to the focus
        view for that object.
        """
        todo = Todo.objects.create(text='test')
        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, todo.text)

    def test_index_view_completed_fraction(self):
        """
        The correct number of completed todos should be shown on the index
        page.
        """
        Todo.objects.create(text='compelte', complete=True)
        Todo.objects.create(text='incomplete')

        response = self.client.get(reverse('todos:index'))

        self.assertContains(response, '1 / 2')


class TodoFocusViewTests(TestCase):
    def test_focus_view_for_a_todo_shows_that_todos_text(self):
        """
        The correct text should be displayed on the screen when in the focus
        view for a particular todo.
        """
        todo = Todo.objects.create(text='tester')

        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, todo.text)

    def test_focus_view_buttons_if_last_task_incomplete(self):
        """
        If the task is the last (or only) in a list and it is not complete,
        there should be a 'Home' button and a 'Complete' button.
        """
        todo = Todo.objects.create(text='test')

        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, 'Complete')
        self.assertContains(response, 'Home')

    def test_focus_view_buttons_if_last_task_complete(self):
        """
        If the task is the last (or only) in a list and it is complete,
        there should only be a 'Home' button.
        """
        todo = Todo.objects.create(text='test', complete=True)

        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, 'Home')

    def test_focus_view_buttons_if_not_last_task_incomplete(self):
        """
        If there are tasks to complete after the current task and the current
        task is not complete, there should be a 'Home' button, a 'Skip' button
        and a 'Complete' button.
        """
        todo = Todo.objects.create(text='test')
        Todo.objects.create(text='test two')

        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, 'Complete')
        self.assertContains(response, 'Skip')
        self.assertContains(response, 'Home')

    def test_focus_view_buttons_if_not_last_task_and_complete(self):
        """
        If there are tasks to complete after the current task and the current
        task is complete, there should be a 'Home' button and a 'Next' button.
        """
        todo = Todo.objects.create(text='test', complete=True)
        Todo.objects.create(text='test two')

        response = self.client.get(reverse('todos:focus', args=((todo.pk,))))

        self.assertContains(response, 'Next')
        self.assertContains(response, 'Home')


class TodoToggleStatusViewTests(TestCase):
    def test_toggle_view_makes_an_incomplete_task_complete(self):
        """
        When navigating to the toggle view, an incomplete todo object should be
        marked as complete.
        """
        todo = Todo.objects.create(text='incomplete')

        self.assertEqual(
            Todo.objects.filter(complete=False).count(),
            1
        )

        self.client.post(reverse('todos:toggle', args=((todo.pk,))))

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            1
        )

    def test_toggle_view_makes_an_complete_task_incomplete(self):
        """
        When navigating to the toggle view, an complete todo object should be
        marked as incomplete.
        """
        todo = Todo.objects.create(text='complete', complete=True)

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            1
        )

        self.client.post(reverse('todos:toggle', args=((todo.pk,))))

        self.assertEqual(
            Todo.objects.filter(complete=False).count(),
            1
        )

    def test_toggle_view_returns_the_correct_json_response(self):
        """
        Using the toggle view should return a json response with the correct
        data.
        """
        todo = Todo.objects.create(text='incomplete')

        response = self.client.post(
            reverse('todos:toggle', args=((todo.pk,)))
        )

        json_string = response.content
        data = json.loads(json_string)

        self.assertTrue(data['complete'])

        response = self.client.post(
            reverse('todos:toggle', args=((todo.pk,)))
        )

        json_string = response.content
        data = json.loads(json_string)

        self.assertFalse(data['complete'])


class TodoCompleteViewTests(TestCase):
    def test_complete_view_makes_given_task_complete_eq_true(self):
        """
        When navigating to the complete view, the todo object should be
        marked as complete.
        """
        todo = Todo.objects.create(text='incomplete')

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            0
        )

        self.client.get(reverse('todos:complete', args=((todo.pk,))))

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            1
        )

    def test_complete_view_redirects_to_focus_view_for_next_todo(self):
        """
        After the complete view's logic has been completed, the client
        should be redirected to the focus view for the todo of the next highest
        priority.
        """
        todo = Todo.objects.create(text='incomplete')
        next_todo = Todo.objects.create(text='next highest priority')

        response = self.client.get(
            reverse('todos:complete', args=((todo.pk,)))
        )

        self.assertRedirects(
            response,
            reverse('todos:focus', args=((next_todo.pk,)))
        )

    def test_complete_view_redirects_to_index_view_if_last_todo(self):
        """
        If navigating to the complete view from the last todo in the list,
        the client should be redirected to the index view.
        """
        todo = Todo.objects.create(text='incomplete')

        response = self.client.get(
            reverse('todos:complete', args=((todo.pk,)))
        )

        self.assertRedirects(
            response,
            reverse('todos:index')
        )


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

        self.client.post(reverse('todos:reset'))

        self.assertEqual(
            Todo.objects.filter(complete=True).count(),
            0
        )

    def test_reset_view_returns_json_response(self):
        """
        After the reset view's logic has been completed, the client
        should be set a JSON
        """
        Todo.objects.create(text='incomplete')

        response = self.client.post(
            reverse('todos:reset')
        )

        json_string = response.content
        data = json.loads(json_string)

        self.assertTrue(data['reset'])
