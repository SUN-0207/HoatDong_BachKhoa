from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from lxml import etree
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
            if self.event_info_major_id.department_id != self.event_department_id or self.event_department_id.name != 'Tất cả':
                self.event_info_major_id = False
      
        return {
            'domain': {'event_info_major_id': domain} 
        }

    @api.onchange('event_info_major_id')
    def _compute_user_info_department(self):
        for record in self:
            if record.event_info_major_id and self.event_info_major_id.name != 'Tất cả':
                record.event_department_id = record.event_info_major_id.department_id

    @api.model
    def create(self, vals):
            #Check dieu kien o day
            print(self)
            print('Create tickets: ', vals)
            event_registration = super(EventTicket, self).create(vals)
            return event_registration

    def write(self, vals):      
        print('Update tickets: ', vals)
   
        return super(EventTicket, self).write(vals)

    def unlink(self):
        # Perform custom logic before deleting the record
        # ...  
        print('Im done')

        # Call the superclass unlink() method to delete the record
        return super(EventTicket, self).unlink()
 
