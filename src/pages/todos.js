/*jshint esnext:true */
import {http}       from '../utils/http';
import {prioritise} from '../utils/prioritise';
import {vars}       from '../utils/variables';
import $            from 'jquery/jquery.min';
import _            from 'lodash';
import Sortable     from 'sortable/Sortable.min';

export class Todos {
    constructor() {
        this.subheading = 'Click on a todo to focus';
        this.todos = {};
        this.newTodoText = '';
    }

    // Fetches and parses the todo JSON from the API
    fetchTodos() {
        return http.get(
            vars.todos_url
        ).then(response => {
            this.parseResponse(response);
        }, () => {
            alert('There was an error fetching the todos');
        });
    }

    // Parse the JSON response
    parseResponse(response) {
        this.todos = JSON.parse(response.response).sort(prioritise);
        this.numcompleted = _.where(this.todos, {'complete': true}).length;
    }

    // Get the todo object for a given ID
    getTodo(id) {
        return _.find(this.todos, 'id', id);
    }

    // Edit the text for a todo
    edit(id, text) {
        let todo = this.getTodo(parseInt(id));

        http.patch(
            vars.todo_url(id),
            {'text': text}
        ).then(response => {
            if (response.isSuccess) {
                $('.todo > .edit').show();
                $('.todo > .focuslink').show();
                $('.todo > .todotextinput').hide();
                todo.text = text;
            }
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }


    // Toggles the status of a todo object
    toggleComplete(id) {
        let todo = this.getTodo(id);
        let status = todo.complete ? false : true;

        http.patch(
            vars.todo_url(id),
            {'complete': status}
        ).then(response => {
            if (response.isSuccess) {
                this.parseResponse(response);
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
            if (response.isSuccess)
                this.parseResponse(response);
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

        let del = confirm(`Delete todo: "${todo.text}"?`);

        if (del) {
            http.delete(
                vars.todo_url(id)
            ).then(response => {
                if (response.isSuccess)
                    this.parseResponse(response);
            }, (error) => {
                console.log(error);
                // TODO: Create error at top of page or something
            });
        }
    }

    // Init the Sortable JS once the page has loaded
    attached() {
        let el = document.getElementById('js-todos');

        new Sortable(el, {
            ghostClass: '-dragging',
            handle: '.priority',
            onUpdate: (ev) => {
                if (ev.oldIndex === ev.newIndex)
                    return;

                let todos = [];

                _.forEach($('.todo'), (todo, i) => {
                    todos.push(
                        {
                            id: parseInt(todo.id.split('todo')[1]),
                            priority: i + 1
                        }
                    );
                });

                http.patch(
                    vars.todos_url,
                    JSON.stringify(todos)
                ).then(response => {
                    if (response.isSuccess)
                        this.parseResponse(response);
                }, (error) => {
                    console.log(error);
                    // TODO: Create error at top of page or something
                });
            },
        });

        // Hide the text and show the input box when editing
        $(window.document).on('click', '.edit', function() {
            $(this).siblings('.focuslink').hide();
            $(this).siblings('.todotextinput').show().focus();
            $(this).hide();
            return false;
        });

        // Fix for cursor placement when setting focus
        $(window.document).on('focus', '.todotextinput', function() {
              this.selectionStart = this.selectionEnd = this.value.length;
        });

        $(window.document).on('keyup', '.todotextinput', (e) => {
            let $this = $(e.target);

            // return
            if (e.keyCode == 13) {
                let id = $this.parent().attr('id').split('todo')[1];
                this.edit(id, $this.val());
            }

            // esc
            if (e.keyCode == 27) {
                $this.siblings('.focuslink').show();
                $this.siblings('.edit').show();
                $this.hide();
            }
        });

        $(window.document).on('blur', '.todotextinput', function() {
            $(this).siblings('.focuslink').show();
            $(this).siblings('.edit').show();
            $(this).hide();
        });

    }

    // Wait for the todos to be fetched before loading the view.
    activate() {
        return this.fetchTodos();
    }

}
