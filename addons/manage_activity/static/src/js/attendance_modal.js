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
          res_model: 'event.attendance.check.wizard',
          name:'Điểm danh sinh viên tham gia',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
          context: {
            'default_event_id': this.props.context.active_id,
            'default_num_a': this.props.context.active_id,
          }
      });
   }
}
registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});

