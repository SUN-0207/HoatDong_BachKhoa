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

    # Khoa field neu chon Tat ca
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form',
    #                     toolbar=False, submenu=False):
    #     res = super(EventTicket, self).fields_view_get(
    #         view_id=view_id, view_type=view_type,
    #         toolbar=toolbar, submenu=submenu)
      
    #     doc = etree.XML(res['arch'])
    #     create_button = doc.xpath("//tree[@create='1']")
            
    #     if create_button and self.event_department_id.name == 'Tat ca':
    #             create_button[0].attrib['create'] = '0'
            
    #     res['arch'] = etree.tostring(doc)
    #     print(res)
    #     return res