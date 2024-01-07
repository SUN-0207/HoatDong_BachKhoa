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
 
    sequence_number = fields.Integer(string='Số thứ tự', store=True, exportable=False)
    
    can_action_on_registration = fields.Boolean(default=False, exportable=False)
    ctxh_max = fields.Float(related='event_id.max_social_point', exportable=False)
    drl_max = fields.Integer(related='event_id.max_tranning_point', exportable=False)

    ctxh = fields.Float(compute='_compute_ctxh', store=True, digits=(16, 1))
    drl = fields.Integer(compute='_compute_drl', store=True, string="ĐRL")

    @api.depends('ctxh_max')
    def _compute_ctxh(self):
        for record in self:
            record.ctxh = record.ctxh_max

    @api.depends('drl_max')
    def _compute_drl(self):
        for record in self:
            record.drl = record.drl_max

    def edit_ctxh_drl(self):
      return {
        'name': 'Cập nhật',
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'event.point.edit.wizard',
        'view_id': False,
        'target': 'new',
        'context': {
            'default_regis_id': self.id,
            'default_ctxh':  self.ctxh,
            'default_drl': self.drl
        }
      }

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
      if('ctxh' in vals):
        if(vals['ctxh'] < 0 ):
          raise ValidationError('CTXH cập nhật phải là số dương')
        if(vals['ctxh'] > self.ctxh_max):
          raise ValidationError('Không thể cập nhật số ngày CTXH lớn hơn CTXH tối đa của hoạt động đã thiết lập!')
      if('drl' in vals):
        if(vals['drl'] < 0 ):
          raise ValidationError('ĐRL cập nhật phải là số dương')
        if(vals['drl'] > self.drl_max):
          raise ValidationError('Không thể cập nhật ĐRL lớn hơn ĐRL tối đa của hoạt động đã thiết lập!')    
      if('time_check_attendace' in vals):
        if(vals['time_check_attendace'] >= self.event_id.min_attendance_check):
          vals['state'] = 'done'
          vals['state_temp'] = 'done'
        else:
          vals['state'] = 'open'
          vals['state_temp'] = 'open'
      return super(EventRegistration, self).write(vals)
    
    def action_set_done(self):
      self.write({'state': 'done'})
      self.time_check_attendace = self.event_id.min_attendance_check
      self.env['event.attendance.check'].create({
            'event_id': self.event_id.id,
            'registration_id': self.id,
            'time_check': self.time_check_attendace,
            'type_action': 'Xác nhận tham gia '
        })

    def attendace(self):
        self.ensure_one()
        self.time_check_attendace += 1
        self.write({'time_check_attendace': self.time_check_attendace})
        
        AttendanceCheckRecord = self.env['event.attendance.check']
        new_record = AttendanceCheckRecord.create({
            'event_id': self.event_id.id,
            'registration_id': self.id,
            'time_check': self.time_check_attendace,
            'type_action': 'Điểm danh '
        })
      

    def delele_latest_check(self):
        self.ensure_one()
        latest_check = self.env['event.attendance.check'].search([
            ('registration_id', '=', self.id),
            ('time_check', '=', self.time_check_attendace)
        ], order='id desc', limit=1)
       
        if latest_check:
            # latest_check.unlink() track lich su thi khong nen unlink
            self.env['event.attendance.check'].create({
              'event_id': self.event_id.id,
              'registration_id': self.id,
              'time_check': self.time_check_attendace,
              'type_action': 'Xóa điểm danh '
              })
            self.time_check_attendace -= 1
            self.write({'time_check_attendace': self.time_check_attendace})

          
