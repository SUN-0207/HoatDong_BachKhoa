odoo.define('user.info.invalid_field', function(require) {
    "use strict";
  
    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
  
    var YourCustomWidget = AbstractField.extend({
      className: 'invalid_field',
  
      init: function() {
        this._super.apply(this, arguments);
      },
  
      _render: function() {
        this.$el.removeClass('error-field'); // Remove previous error class if any
  
        var value = this.value;
        var pattern = /^0?\d{7}$/;
        if (!value || !pattern.test(value)) {
          this.$el.addClass('error-field'); // Apply error class
        }
        this.$el.text(value);
      }
    });
  
    field_registry.add('invalid_input_field', YourCustomWidget);
  
    return YourCustomWidget;
  });