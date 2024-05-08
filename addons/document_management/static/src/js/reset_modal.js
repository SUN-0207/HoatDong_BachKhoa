/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
export class SaleListController extends ListController {
   setup() {
       super.setup();
   }
   OnTestClick() {
      this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'document.reset.number.book.wizard',
          name:'Đặt lại số kí hiệu',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
      });
   }
}
registry.category("views").add("button_reset_document", {
    ...listView,
    Controller: SaleListController,
    buttonTemplate: "button_reset_document.ListView.Buttons",
});


