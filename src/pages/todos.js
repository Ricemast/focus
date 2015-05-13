/*jshint esnext:true */
import {HttpClient} from 'aurelia-http-client';

import {prioritise} from '../utils/prioritise';
import {toggleComplete} from '../utils/toggleComplete';

// Create a consts file with all urls in
const todos_url = '/todos/';

export class Todos {
    static inject() { return [HttpClient]; }

    constructor(http) {
        this.http = new HttpClient().configure(x => {
            x.withBaseUrl('http://127.0.0.1:8000');
            x.withHeader('Content-Type', 'application/json');
        });

        this.subheading = 'Click on a todo to focus';
        this.todos = {};
        this.numcompleted = 0;
    }

    // Fetches and parses the todo JSON from the API
    fetchTodos() {
        this.http.get(todos_url).then(response => {
            let count = 0;
            let todos = JSON.parse(response.response).sort(prioritise);

            todos.forEach(todo => {
                todo.toggleComplete = toggleComplete;
                count += todo.complete ? 1 : 0;
            });

            this.todos = todos;
            this.numcompleted = count;
        }, () => {
            alert('There was an error fetching the todos');
        });
    }

    // Toggles the status of a todo object
    toggleComplete(id) {
        let put_url = `/todos/${id}/`;
        let todo = this.todos.filter(function(todo) {
            return todo.id == id;
        })[0];

        if (!todo) {
            console.log('Error, no todo with that ID exists');
            return;
        }

        let status = todo.complete ? false : true;

        this.http.patch(put_url, {'complete': status}).then(response => {
            if (response.isSuccess)
                todo.complete = status;
                this.numcompleted += status ? 1 : -1;
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

        this.http.patch(
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

    // Runs before the view is displayed
    activate() {
        this.fetchTodos();
    }

}
