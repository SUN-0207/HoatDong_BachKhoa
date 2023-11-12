odoo.define('manage_activity.create_ticket', function (require) {
    "use strict";
    
    var ListRenderer = require("web.ListRenderer");
    var ListView = require("web.ListView");
    var viewRegistry = require("web.view_registry");

    var CustomListRenderer = ListRenderer.extend({
        _renderRow : function (record) {
            console.log('Huy')
        }
    }) 

    var CustomListView = ListView.extend({
        config: _extend({}, ListView.prototype.config, {
            Renderer: CustomListRenderer,
        })
    });

    viewRegistry.add("create_ticket", CustomListView)
    
    
    
 });