$(function() {

    // Helper function for submitting a POST request to a django view.
    function ajaxSubmit(href, successCallback, data) {

        if (!data)
            data = {};

        // Get the CSRF token from the page. Should be included in the
        // template: {% csrf_token %}
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        if (csrf.length === 0) {
            alert('CSRF Token not found');
            return;
        }

        data.csrfmiddlewaretoken = csrf;

        $.post(
            href,
            data
        ).done(function(response) {
            successCallback(response);
        }).fail(function(response) {
            alert('POST failed. See console for response.');
            console.log(response);
        });

        return;
    }

    // Helper function for updating the todo DOM element from
    // a JSON response
    function updateTodo(response) {
        var todo = $('#todo' + response.pk);
        if (response.complete) {
            todo.addClass('-complete');
            todo.find('.checkbox > i')
                .addClass('fa-check-square')
                .removeClass('fa-square');
        } else {
            todo.removeClass('-complete');
            todo.find('.checkbox > i')
                .addClass('fa-square')
                .removeClass('fa-check-square');
        }

        updateNumberCompleted(response.numcompleted);
    }

    // Helper function for reseting the UI for all of the todo elements.
    function resetTodos(response) {
        if (response.reset) {
            $('.task').each(function() {
                $(this).removeClass('-complete')
                       .find('.checkbox > i')
                       .removeClass('fa-check-square')
                       .addClass('fa-square');
            });
        } else {
            alert('Error with reseting todos');
        }

        updateNumberCompleted(response.numcompleted);
    }

    // Helper function for updating the UI for the number of completed
    // items on the index page.
    function updateNumberCompleted(number) {
        $('.js-numcompleted').text(number);
    }

    // Helper function for updating the UI for the number of completed
    // items on the index page.
    function temp(response) {
        if (response.reordered) {
            $('.task').each(function(i) {
                $(this).find('.priority').text(i + 1);
            });
        } else {
            alert('Error with reseting todos');
        }
    }

    // Quick complete toggle handler
    $('.js-toggle').click(function(e) {
        e.preventDefault();
        ajaxSubmit($(this).data('href'), updateTodo);
    });

    // Reset all todos handler
    $('.js-reset').click(function(e) {
        e.preventDefault();
        ajaxSubmit($(this).attr('href'), resetTodos);
    });

    $(".tasks").sortable({
        ghostClass: '-dragging',
        onEnd: function () {
            var data = {};
            $('.task').each(function(i) {
                var id = $(this).attr('id').split('todo')[1];
                data[id] = i + 1;
            });
            ajaxSubmit('/reorder/', temp, data);
        },
    });

});
