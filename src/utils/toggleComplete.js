/*jshint esnext:true */

// Helper function for handling quick status changes of todos.
// This function is attached to each todo object.
export function toggleComplete() {
    let status = true;
    let url = `http://127.0.0.1:8000/todos/${this.id}/`;


    if (this.complete)
        status = false;

    this.http.put(url, {'complete': status}).then(response => {
        console.log(response);
    }, () => {
        alert('There was an error fetching the todos');
    });
}
