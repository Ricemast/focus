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

        self.assertEqual(todo.next, todo2.id)

    def test_previous_prop_with_single_todo(self):
        """
        The previous property on Todo should return None if it is the only
        (first) todo object.
        """
        todo = Todo.objects.create(text='test')

        self.assertIsNone(todo.previous)

    def test_previous_prop_with_multiple_todos(self):
        """
        The previous property on Todo should return the todo object with the
        previous highest priority if there is one.
        """
        todo = Todo.objects.create(text='test')
        todo2 = Todo.objects.create(text='test2')

        self.assertEqual(todo2.previous, todo.id)


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

    def test_create_a_todo_with_no_priority_and_gaps_in_priorities(self):
        """
        Bug #8: A todo will be created with the priority eq to the lowest
        available priority. This should not be the case. It should be created
        with priority higher than all other todos. i.e. the end of the list.
        """
        Todo.objects.create(text='test', priority=2)
        todo = Todo.objects.create(text='priority3')

        self.assertEqual(todo.priority, 3)
