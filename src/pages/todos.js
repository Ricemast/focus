/*jshint esnext:true */
import {HttpClient} from 'aurelia-http-client';
import {prioritise} from '../utils/prioritise';

const url = 'http://127.0.0.1:8000/api/todo/?format=json';

export class Todos {
    static inject() { return [HttpClient]; }

    constructor(http) {
        this.http = http;
        this.subheading = 'Click on a todo to focus';
        this.todos = {};
    }

    // Fetches and parses the todo JSON from the API
    fetchTodos() {
        this.http.get(url).then(response => {
            this.todos = JSON.parse(response.response).objects.sort(prioritise);

        });
    }

    // Runs before the view is displayed
    activate() {
        this.fetchTodos();
    }

}
