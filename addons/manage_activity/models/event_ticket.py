from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class EventTicket(models.Model):
    _inherit = 'event.type.ticket'
       
    event_department_id = fields.Many2one('user.info.department', string='Đơn vị', store=True)
    event_info_major_id = fields.Many2one('user.info.major',string='Ngành', 
        store=True, domain=lambda self: self._compute_major_domain())
    event_info_academy_year = fields.Many2one('user.info.year', string='Niên khoá', store=True)

    @api.onchange('event_department_id')
    def _compute_major_domain(self):
        domain = []
        if self.event_department_id:
            domain = ['|',('department_id', '=', self.event_department_id.id),('show_student_form', '=', False)]
            if self.event_info_major_id.department_id != self.event_department_id or self.event_department_id.name != 'Tat ca':
                self.event_info_major_id = False
      
        return {
            'domain': {'event_info_major_id': domain} 
        }

    @api.onchange('event_info_major_id')
    def _compute_user_info_department(self):
        for record in self:
            if record.event_info_major_id and self.event_info_major_id.name != 'Tat ca':
                record.event_department_id = record.event_info_major_id.department_id
            

    ticket_department_selection = fields.Selection(string='Ticket Major Selection', selection='_get_ticket_department_selection_options',)
    ticket_major_selection = fields.Selection(string='Ticket Major Selection', selection='_get_ticket_major_selection_options',)
    ticket_academy_year_selection = fields.Selection(string='Ticket Major Selection', selection='_get_ticket_year_selection_options',)

    @api.model
    def _get_ticket_department_selection_options(self):
        selection = [('False', 'Tất cả')]
        department_ids = self.env['user.info.department'].search([]).ids
        selection += [(str(department_id), self.env['user.info.department'].browse(department_id).display_name) for department_id in department_ids]
        print(selection)
        return selection   