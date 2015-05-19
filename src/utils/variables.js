/*jshint esnext:true */

const json = '?format=json';

export let vars = {
    backend_url: 'http://192.168.1.65:8000',
    todos_url: `/todos/${json}`,
    todo_url: function(id) {
        return `todos/${id}/${json}`;
    }
};
