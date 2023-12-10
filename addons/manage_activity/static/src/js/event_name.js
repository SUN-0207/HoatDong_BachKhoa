$(document).ready(function () {
    var name_input = $('.event-name-group .o_field_widget input');
    var nameVal = name_input.val();
    if (nameVal !== "") {
      name_input.parents('.o_field_widget').addClass('has_name');
    }

    $('.event-name-group .o_field_widget input').on('blur', function () {
        var nameVal = $(this).val();
        if (nameVal !== "") {
            $(this).parents('.o_field_widget').addClass('has_name');
            console.log('event has name');
        } else {
            $(this).parents('.o_field_widget').removeClass('has_name');
            console.log('event doesnt have name');
        }
    });

    $('.o_form_button_cancel').on('click', function () {
      name_input.parents('.o_field_widget').addClass('has_name');
    })
});

$(document).on('keydown', function(event) {
    if (event.key === 'Enter' && $(document.activeElement).is('#mssv')){
        event.preventDefault();
        $('#mssv').blur();
        $('#submit').click();
        setTimeout(function() {
            $('#mssv').val('');
        }, 250);
        setTimeout(function() {
            $('#mssv').focus();
        }, 250);
    }
    else if (event.key === 'Enter' && event.currentTarget.location.hash.includes('model=event.registration&view_type=list' )) {
        event.preventDefault();
        $('#submit').click();
        setTimeout(function() {
            $('#mssv').val('');
        }, 250);
        setTimeout(function() {
            $('#mssv').focus();
        }, 250);
    }
});