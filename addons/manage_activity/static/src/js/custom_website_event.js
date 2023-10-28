
odoo.define('manage_activity.custom_website_event', function (require) {
    "use strict";

    console.log('111XXX');

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    var WebsiteEvent = require('website_event.website_event')
    var _t = core._t;
    
    var inheritEventRegistrationForm = WebsiteEvent.include({
        
    })
    // Catch registration form event, because of JS for attendee details
    var inheritEventRegistrationForm = WebsiteEvent.include({
        events: _.extend({}, WebsiteEvent.prototype.events, {
            'click .registration_button': 'on_click',
        }),
    
    
        on_click: function (ev) {
            var self = this;
            ev.preventDefault();
            ev.stopPropagation();
            var $form = $(ev.currentTarget).closest('form');
            var $button = $(ev.currentTarget).closest('[type="submit"]');
            var post = {};
            $('#registration_form table').siblings('.alert').remove();
            $('#registration_form select').each(function () {
                post[$(this).attr('name')] = $(this).val();
            });
            console.log('Registration button clicked');
            console.log('Form:', $form);
            console.log('Post Data:', post);
            
            return ajax.jsonRpc($form.attr('action'), 'call', post).then(function (modal) {
                var $modal = $(modal);
                $modal.find('.modal-body > div').removeClass('container'); // retrocompatibility - REMOVE ME in master / saas-19
                $modal.appendTo(document.body);
                const modalBS = new Modal($modal[0], {backdrop: 'static', keyboard: false});
                modalBS.show();
                
                $modal.appendTo('body').modal('show');
                $modal.on('click', '.js_goto_event', function () {
                    $modal.modal('hide');
                    $button.prop('disabled', false);
                });
                $modal.on('click', '.btn-close', function () {
                    $button.prop('disabled', false);
                });
                console.log('Form:', $modal);
            });

        },
    });

    return inheritEventRegistrationForm;
});