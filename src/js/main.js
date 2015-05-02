$(function() {

    // Quick complete toggle handler
    $('.js-toggle').click(function() {

        var $this = $(this);
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

        $.post(
            $this.data('href'),
            { csrfmiddlewaretoken: csrf }
        ).done(function(data) {
            if (data.complete) {
                $this.parent().addClass('-complete');
                $this.find('i')
                     .addClass('fa-check-square')
                     .removeClass('fa-square');
            } else {
                $this.parent().removeClass('-complete');
                $this.find('i')
                     .addClass('fa-square')
                     .removeClass('fa-check-square');
            }

            $('.js-numcompleted').text(data.numcompleted);
        });

        return false;
    });

    // Reset all todos handler
    $('.js-reset').click(function() {

        var csrf = $('input[name="csrfmiddlewaretoken"]').val();

        $.post(
            $(this).attr('href'),
            { csrfmiddlewaretoken: csrf }
        ).done(function(data) {
            if (data.reset) {
                $('.task').each(function() {
                    $(this).removeClass('-complete')
                           .find('.checkbox > i')
                           .removeClass('fa-check-square')
                           .addClass('fa-square');
                });
            } else {
                alert('Error with reseting todos');
            }

            $('.js-numcompleted').text(data.numcompleted);
        });

        return false;
    });

});
