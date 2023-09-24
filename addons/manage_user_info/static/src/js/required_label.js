odoo.define('manage_user_info.custom_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var core = require('web.core');
    var _t = core._t;

    FormController.include({
        init: function () {
            this._super.apply(this, arguments);
            this._setupCustomValidation();
        },

        _setupCustomValidation: function () {
            var self = this;
            var field = this.renderer.state.fields.personal_email;
            console.log(field)
            if (field) {
                field.$el.on('blur', function () {
                    var email = field.$el.val();
                    console.log(email)
                    if (email && !validateEmail(email)) {
                        self.displayNotification({
                            type: 'danger',
                            title: _t("Invalid Email"),
                            message: _t("Please enter a valid email address."),
                            sticky: false
                        });
                    }
                });
            }
        },
    });

    function validateEmail(email) {
        // Regular expression for email validation
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});