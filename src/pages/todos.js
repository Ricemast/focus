/*jshint esnext:true */
import {HttpClient} from 'aurelia-http-client';

import {prioritise} from '../utils/prioritise';
import {toggleComplete} from '../utils/toggleComplete';

const url = 'http://127.0.0.1:8000/api/todo/?format=json';

export class Todos {
    static inject() { return [HttpClient]; }

    constructor(http) {
        this.http = http;
        this.subheading = 'Click on a todo to focus';
        this.todos = {};
        this.numcompleted = 0;
    }

    // Fetches and parses the todo JSON from the API
    fetchTodos() {
        this.http.get(url).then(response => {
            let count = 0;
            let todos = JSON.parse(response.response).objects.sort(prioritise);

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

    // Resets all the todos to be incomplete
    resetTodos() {
        this.todos.forEach(todo => {
            todo.complete = false;
        });
    }

    // Runs before the view is displayed
    activate() {
        this.fetchTodos();
    }

}
