from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class EventTicket(models.Model):
    _inherit = 'event.type.ticket'
    
    event_department_id = fields.Many2one('user.info.department', string='Đơn vị', store=True)
    event_info_major_id = fields.Many2one('user.info.major',string='Ngành', store=True)
    event_info_academy_year = fields.Many2one('user.info.year', string='Niên khoá', store=True)
 
    @api.depends('event_info_major_id')
    def _compute_ticket_info_department(self):
        for record in self:
            if record.event_info_major_id :
                record.event_department_id = record.event_info_major_id.department_id
            else:
                record.event_department_id = False