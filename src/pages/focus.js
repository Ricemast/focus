/*jshint esnext:true */
import {HttpClient} from 'aurelia-http-client';

export class Focus {
    static inject() { return [HttpClient]; }

    constructor(http) {
        this.http = new HttpClient().configure(x => {
            x.withBaseUrl('http://127.0.0.1:8000');
            x.withHeader('Content-Type', 'application/json');
        });

        this.todo = {};
    }

    // Fetches and parses the todo JSON from the API
    fetchTodo(id) {
        let todo_url = `/todos/${id}/`;

        return this.http.get(todo_url).then(response => {
            this.todo = JSON.parse(response.response);
        }, () => {
            alert('There was an error fetching the todo.');
        });
    }

    toggle() {
        this.todo.complete = this.todo.complete ? false : true;
    }

    // Get the todo before rendering the view
    activate(params) {
        return this.fetchTodo(params.id);
    }

}
