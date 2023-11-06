
odoo.define('manage_activity.custom_website_event', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var publicWidget = require('web.public.widget');
    var WebsiteEvent = require('website_event.website_event')
    var _t = core._t;
    

    // Catch registration form event, because of JS for attendee details
    var inheritEventRegistrationForm = WebsiteEvent.include({
        // start: function () {
        //     var self = this;
        //     var event_id = self.$('#registration_form').data('event-id');
        //     var partner_id = self.$('#registration_form').data('partner-id');
        //     console.log(this)
        //     console.log(event_id)
        //     console.log(partner_id)
            // var res = this._super.apply(this, arguments).then(function () {
            //     var $submitButton = self.$('#registration_form .a-submit');
            //     var registrationPromise = self._rpc({
            //         route: '/event/check_user_registration',
            //         params: {
            //             event_id: event_id,
            //             partner_id: partner_id,
            //         },
            //     });
        
            //     return $.when(registrationPromise).then(function (result) {
            //         if (result.is_registered) {
            //             $submitButton.hide();
            //         } else {
            //             $submitButton.prop('disabled', false);
            //         }
            //     });
            // });
        
            // return res;
        // },

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