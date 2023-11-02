from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class EventTicket(models.Model):
    _inherit = 'event.type.ticket'
       
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

    #Not working
    # @api.onchange('ticket_department_selection')
    # def _change_selection_for_ticket_major_selection(self):
    #     if self.ticket_department_selection != 'False':
    #         domain = [('department_id', '=', int(self.ticket_department_selection))]
    #         major_ids = self.env['user.info.major'].search(domain)
    #         selection = [('False', 'Tất cả')] + [(str(major_id), major_id.name) for major_id in major_ids]
    #         return {'domain': {'ticket_major_selection': selection}}
    #     else:
    #         return {'domain': {'ticket_major_selection': []}}

    @api.model
    def _get_ticket_major_selection_options(self):
        selection = [('False', 'Tất cả')]
        major_ids = self.env['user.info.major'].search([]).ids
        selection += [(str(major_id), self.env['user.info.major'].browse(major_id).name) for major_id in major_ids]
        return selection

    @api.onchange('ticket_major_selection')
    def _match_correct_department_of_major_selected(self):
        if self.ticket_major_selection != 'False':
            major = self.env['user.info.major'].browse(int(self.ticket_major_selection))
            if major:
                self.ticket_department_selection = str(major.department_id.id)
    

    @api.model
    def _get_ticket_year_selection_options(self):
        selection = [('False', 'Tất cả')]
        academy_years_ids = self.env['user.info.year'].search([]).ids
        selection += [(str(academy_years_id), self.env['user.info.year'].browse(academy_years_id).name) for academy_years_id in academy_years_ids]
        return selection