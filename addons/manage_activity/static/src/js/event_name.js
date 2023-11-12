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

// odoo.define('manage_activity.event_name', function (require) {
//     "use strict";

//     var core = require('web.core');
//     var $ = require('jquery');

//     console.log("uqyayauayyay")

    // $(document).ready(function () {
    //     $('.event-name-group .o_field_widget input').on('blur', function () {
    //         var nameVal = $(this).val();
    //         if (nameVal !== "") {
    //             $(this).parents('.o_field_widget').addClass('has_name');
    //             console.log('event has name');
    //         } else {
    //             $(this).parents('.o_field_widget').removeClass('has_name');
    //         }
    //     });
    // });
// });

    