/*jshint esnext:true */
//
// Helper function for handling quick status changes of todos.
// This function is attached to each todo object.
export function toggleComplete() {
    if (this.complete)
        this.complete = false;
    else
        this.complete = true;
}
