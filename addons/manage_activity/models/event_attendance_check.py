from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventAttendanceCheck(models.Model):
    _name = 'event.attendance.check'

    event_id = fields.Many2one('event.event', string='Event', readonly=True)

    user_info_id = fields.Many2one('user.info', string='Thông tin')
    user_info_name = fields.Char(related='user_info_id.name')
    user_info_mssv = fields.Char(string='MSSV')
    
    
    # def register_check(self, vals):
    #     if vals['user_info_mssv']:
    #         raise ValidationError("User is not registered for the event.")
    #     return

    # @api.model
    # def create(self, vals):
    #     self.register_check(vals)
    #     return super(EventAttendanceCheck, self).create(vals)
    def attendace(self):
        return
    # def attendance_check(self):
    #     self.ensure_one()
    #     return {
    #         'name': 'Diem danh',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'res_model': 'event.attendance.check',
    #         'type': 'ir.actions.act_window',
    #         'target': 'current',
    #         'context': {'form_view_ref': 'event_attendance_check_form_view'},
    #     }