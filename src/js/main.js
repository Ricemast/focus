$(function() {

    $('.task > .toggle').click(function() {

        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        var $this = $(this);

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

        });

        return false;
    });

});
