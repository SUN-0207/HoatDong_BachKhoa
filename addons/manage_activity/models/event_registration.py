from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventRegistration(models.Model):
    _inherit = ['event.registration']
              
    user_info_id = fields.Many2one('user.info', string='Thông tin')
    user_info_name = fields.Char(related='user_info_id.name')
    user_info_mssv = fields.Char(string='MSSV', related='user_info_id.student_id')
    user_department_id = fields.Many2one('user.info.department', string='Đơn vị', related='user_info_id.user_info_department_id',readonly=True, store=True)
    
    time_check_attendace = fields.Integer('So lan diem danh', default=0)
    state_temp = fields.Selection([
        ('draft', 'Đăng ký'), ('cancel', 'Từ chối'),
        ('open', 'Chấp nhận'), ('done', 'Đã tham gia')],
        string='Trạng thái', default='draft', readonly=True, tracking=True, compute='_compute_state')
    
    sequence_number = fields.Integer(string='Số thứ tự', store=True)
    
    can_action_on_registration = fields.Boolean(default=False)
    
    @api.depends('state')
    def _compute_state(self):
      for registration in self:
        self.state_temp = registration.state
        
    def multi_confirmation(self):
      for registration in self:
        if not registration.can_action_on_registration:
          raise ValidationError("Yêu cầu quyền duyệt từ Quản trị viên")
        if registration.state != 'draft':
          raise ValidationError("Chỉ áp dụng đối với sinh viên có trạng thái là ĐĂNG KÝ")
        registration.sudo().action_confirm()
      
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=0):
      records = super(EventRegistration, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
      if records:
        for record in records: 
          event_id = record['event_id'][0]
          if self.env.user.has_group('manage_user_info.group_hcmut_super_admin') or self.env['event.event'].sudo().search([('id', '=', event_id),('created_by_name', '=', self.env.user.name)]):
            record['can_action_on_registration'] = True
          else:
            record['can_action_on_registration'] = False
      return records
      
    @api.model
    def create(self,vals):
      current_event_registration_count = self.search_count([('event_id','=',vals['event_id'])])
      vals['sequence_number'] = current_event_registration_count + 1
      return super(EventRegistration, self).create(vals)
    
    @api.model
    def write(self,vals):
      if('time_check_attendace' in vals):
        if(vals['time_check_attendace'] >= self.event_id.min_attendance_check):
          vals['state'] = 'done'
        
      return super(EventRegistration, self).write(vals)
    
    def attendace(self):
        self.time_check_attendace += 1
        self.write({'time_check_attendace': self.time_check_attendace})
        
        AttendanceCheckRecord = self.env['event.attendance.check']
        new_record = AttendanceCheckRecord.create({
            'event_id': self.event_id.id,
            'registration_id': self.id,
            'time_check': self.time_check_attendace
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Điểm danh thành công',
                'type': 'success',
                'sticky': False,
            },
        }
          
