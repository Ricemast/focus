/*jshint esnext:true */
import {http}       from '../utils/http';
import {prioritise} from '../utils/prioritise';
import {vars}       from '../utils/variables';

export class Todos {
    constructor() {
        this.subheading = 'Click on a todo to focus';
        this.todos = {};
        this.numcompleted = 0;
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

    // Toggles the status of a todo object
    toggleComplete(id) {
        let todo = this.todos.filter(function(todo) {
            return todo.id == id;
        })[0];

        if (!todo) {
            console.log('Error, no todo with that ID exists');
            return;
        }

        let status = todo.complete ? false : true;

        http.patch(vars.todo_url(id), {'complete': status}).then(response => {
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
            '/todos/reset/',
            JSON.stringify(todos)
        ).then(response => {
            if (response.isSuccess)
                this.todos = todos;
                this.numcompleted = 0;
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }

    // Wait for the todos to be fetched before loading the view.
    activate() {
        return this.fetchTodos();
    }

}
