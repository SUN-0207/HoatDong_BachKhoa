from odoo import fields, models

class EventPointEditWizard(models.TransientModel):
    _name = "event.point.edit.wizard"
    regis_id = fields.Many2one('event.registration')
    sv_name = fields.Char(related='regis_id.user_info_name')
    event_name = fields.Many2one('event.event',related='regis_id.event_id')
    ctxh = fields.Float()
    drl = fields.Integer()

    def confirm_edit(self):
        self.ensure_one()

        self.regis_id.write({
            'ctxh': self.ctxh,
            'drl': self.drl
        })
        return self.notify_success()

    def notify_success(self):
      return {
          'type': 'ir.actions.client',
          'tag': 'display_notification',
          'params': {
              'title': 'Thành công',
              'message': 'Thao tác của bạn đã được lưu',
              'type': 'success',
              'sticky': False, 
              'next': {'type': 'ir.actions.act_window_close'},
          },
      }
 
  