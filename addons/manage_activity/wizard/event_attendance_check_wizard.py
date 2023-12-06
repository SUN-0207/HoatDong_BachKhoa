from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class EventAttendanceCheckWizard(models.TransientModel):
    _name = "event.attendance.check.wizard"
    
    event_id = fields.Many2one('event.event', string='Event', readonly=True)
    mssv = fields.Char(string="MSSV")
    # name = fields.Char(string="Name", readonly=True, compute='find_name')

    # @api.depends('mssv')
    # def find_name(self):
    #     for record in self:
    #         print(record.mssv)
    #         print(self.env['event.registration'].search([('user_info_mssv','=', record.mssv)],limit=1).user_info_name)
    #         record.name = self.env['event.registration'].search([('user_info_mssv','=', record.mssv)],limit=1).user_info_name


    def attendance_check(self):
        self.ensure_one()
        print('@@@@@@@@@@22', self.event_id)
        return self.notify_success

    
    def notify_success(self):
      return {
          'type': 'ir.actions.client',
          'tag': 'display_notification',
          'params': {
              'title': 'Thành công',
              'message': 'Thao tác của bạn đã được lưu',
              'type': 'success',
              'sticky': False
          },
      }
    