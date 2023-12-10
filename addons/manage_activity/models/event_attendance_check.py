from odoo import models, fields
from odoo.exceptions import ValidationError

class EventAttendanceCheck(models.Model):
    _name = 'event.attendance.check'

    event_id = fields.Many2one('event.event', string='Event', readonly=True)
    registration_id = fields.Many2one('event.registration', readonly=True)
    user_info_id = fields.Many2one('user.info', string='Thông tin')
    user_info_name = fields.Char(related='registration_id.user_info_name')
    user_info_mssv = fields.Char(related='registration_id.user_info_mssv')

    time_check = fields.Integer(string='Điểm danh lần thứ')