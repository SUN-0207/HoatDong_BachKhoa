from odoo import models, fields
from odoo.exceptions import ValidationError

class EventAttendanceCheck(models.Model):
    _name = 'event.attendance.check'

    event_id = fields.Many2one('event.event', string='Event', readonly=True)

    user_info_id = fields.Many2one('user.info', string='Thông tin')
    user_info_name = fields.Char(related='user_info_id.name')
    user_info_mssv = fields.Char(related='user_info_id.student_id')