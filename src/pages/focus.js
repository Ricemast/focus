/*jshint esnext:true */
import {http} from '../utils/http';
import {vars} from '../utils/variables';

export class Focus {
    constructor() {
        this.todo = {};
    }

    // Fetches and parses the todo JSON from the API
    fetchTodo(id) {
        return http.get(vars.todo_url(id)).then(response => {
            this.todo = JSON.parse(response.response);
        }, () => {
            alert('There was an error fetching the todo.');
        });
    }

    toggleComplete() {
        let status = this.todo.complete ? false : true;

        http.patch(
            vars.todo_url(this.todo.id),
            {'complete': status}
        ).then(response => {
            if (response.isSuccess)
                this.todo.complete = status;
        }, (error) => {
            console.log(error);
            // TODO: Create error at top of page or something
        });
    }

    // Get the todo before rendering the view
    activate(params) {
        return this.fetchTodo(params.id);
    }

}
