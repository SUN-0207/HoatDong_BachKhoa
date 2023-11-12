from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventRegistration(models.Model):
    _inherit = ['event.registration']
              
    user_info_id = fields.Many2one('user.info', string='Thông tin')
    user_department_id = fields.Many2one('user.info.department', string='Đơn vị', related='user_info_id.user_info_department_id',readonly=True, store=True)
    
    state_temp = fields.Selection([
        ('draft', 'Đăng ký'), ('cancel', 'Từ chối'),
        ('open', 'Chấp nhận'), ('done', 'Đã tham gia')],
        string='Trạng thái', default='draft', readonly=True, tracking=True, compute='_compute_state')
    
    sequence_number = fields.Integer(string='Số thứ tự', store=True)
    
    @api.depends('state')
    def _compute_state(self):
      for registration in self:
        self.state_temp = registration.state
        
    def multi_confirmation(self):
      for registration in self:
        if registration.state != 'draft':
          raise ValidationError("Chỉ áp dụng đối với sinh viên có trạng thái là ĐĂNG KÝ")
        registration.sudo().action_confirm()
      print("Success")

    @api.model
    def create(self,vals):
      print("Create Registration", vals)
      current_event_registration_count = self.search_count([('event_id','=',vals['event_id'])])
      vals['sequence_number'] = current_event_registration_count + 1
      return super(EventRegistration, self).create(vals)
    
    @api.model
    def write(self,vals):
      print("Update Registration", vals)
      return super(EventRegistration, self).write(vals)
    
          
