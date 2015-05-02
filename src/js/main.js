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
                $this.html('\u2714');
            } else {
                $this.parent().removeClass('-complete');
                $this.html('\u2718');
            }

        });

        return false;
    });

});
