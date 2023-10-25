from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class EventTicket(models.Model):
    _inherit = 'event.type.ticket'
    
    is_maximize_department = fields.Boolean(string="Giới hạn đơn vị tham gia", default=False)
    is_maximize_major = fields.Boolean(string="Giới hạn chuyên ngành tham gia", default=False)
    is_maximize_year = fields.Boolean(string="Giới hạn khoá tham gia", default=False)
    event_department_id = fields.Many2one('user.info.department', string='Đơn vị', store=True)
    event_info_major_id = fields.Many2one('user.info.major',string='Ngành', store=True)
    event_info_academy_year = fields.Many2one('user.info.year', string='Niên khoá', store=True)
 