/*jshint esnext:true */

const json = '?format=json';

export let vars = {
    backend_url: 'http://127.0.0.1:8000',
    todos_url: `/todos/${json}`,
    todo_url: function(id) {
        return `todos/${id}/${json}`;
    },
    reset_url: `todos/reset/${json}`
};
