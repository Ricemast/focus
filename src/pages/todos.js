/*jshint esnext:true */
import {http}       from '../utils/http';
import {prioritise} from '../utils/prioritise';
import {vars}       from '../utils/variables';
import $            from 'jquery/jquery.min';
import Sortable     from 'sortable/Sortable.min';

export class Todos {
    constructor() {
        this.subheading = 'Click on a todo to focus';
        this.todos = {};
        this.numcompleted = 0;
        this.newTodoText = '';
    }

    // Fetches and parses the todo JSON from the API
    fetchTodos() {
        return http.get(vars.todos_url).then(response => {
            this.todos = JSON.parse(response.response).sort(prioritise);

            let count = 0;
            this.todos.forEach(todo => {
                count += todo.complete ? 1 : 0;
            });
            this.numcompleted = count;
        }, () => {
            alert('There was an error fetching the todos');
        });
    }

    // Get the todo object for a given ID
    getTodo(id) {
        return this.todos.filter(function(todo) {
            return todo.id == id;
        })[0];
    }

    // Toggles the status of a todo object
    toggleComplete(id) {
        let todo = this.getTodo(id);

        if (!todo) {
            console.log('Error, no todo with that ID exists');
            return;
        }

        let status = todo.complete ? false : true;

        http.patch(
            vars.todo_url(id),
            {'complete': status}
        ).then(response => {
            if (response.isSuccess) {
                todo.complete = status;
                this.numcompleted += status ? 1 : -1;
            }
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }

    // Resets all the todos to be incomplete
    resetTodos() {
        let todos = this.todos;

        todos.forEach(todo => {
            todo.complete = false;
        });

        http.patch(
            vars.todos_url,
            JSON.stringify(todos)
        ).then(response => {
            if (response.isSuccess) {
                this.todos = todos;
                this.numcompleted = 0;
            }
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }

    // Add new todo
    addTodo() {
        let priority = this.todos.length + 1;

        let todo = {
            text: this.newTodoText,
            priority: priority
        };

        http.post(
            vars.todos_url,
            JSON.stringify(todo)
        ).then(response => {
            todo = JSON.parse(response.response);
            if (response.isSuccess) {
                this.todos.push(todo);
                this.newTodoText = '';
            }
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }

    // Delete todo
    deleteTodo(id) {
        let todo = this.getTodo(id);

        let del = http.delete(
            vars.todo_url(id)
        ).then(response => {
            if (response.isSuccess) {
                let i = this.todos.indexOf(todo);
                if(i != -1) {
                    this.todos.splice(i, 1);
                    this.checkOrder(todo.id);
                }
            }
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }

    // Re-order each of the todos
    // @int exludeId is the ID of a todo object to ignore in the check,
    // this is to combat the difference in DOM and data.
    checkOrder(excludeId) {
        let t = this;
        let priority = 1;

        $('.todo').each(function() {
            let id = $(this).attr('id').split('todo')[1];
            if (id != excludeId) {
                let todo = t.getTodo(parseInt(id));
                todo.priority = priority;
                priority += 1;
            }
        });
    }

    // Init the Sortable JS once the page has loaded
    attached() {
        let el = document.getElementById('js-todos');
        let todos = this.todos;
        let t = this;

        new Sortable(el, {
            ghostClass: '-dragging',
            onEnd: function () {
                t.checkOrder();

                http.patch(
                    vars.todos_url,
                    JSON.stringify(todos)
                ).then(response => {
                    if (response.isSuccess)
                        this.todos = todos;
                }, (error) => {
                    console.log(error);
                    // TODO: Create error at top of page or something
                });
            },
        });
    }

    // Wait for the todos to be fetched before loading the view.
    activate() {
        return this.fetchTodos();
    }

}
