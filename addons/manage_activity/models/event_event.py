from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
class EventEvent(models.Model):
  _name = 'event.event'
  _inherit = [
        'event.event'
    ]
  stage_name = fields.Char(string='Ten hoat dong',related='stage_id.name')
  status_activity = fields.Selection(string="Tình trạng hoạt động",
    selection=[
      ('new', 'Mới'),
      ('open_registration', 'Mở đăng ký'),
      ('close_registration', 'Đóng đăng ký'),
      ('inprogress', 'Đang diễn ra'),
      ('completed', 'Đã kết thúc')],
    copy=False,
    default=False,
    store=True,
    tracking=True, 
    compute='_compute_status_activity'
  )
  
  user_id = fields.Many2one('res.users', string='User', readonly=True, default=lambda self: self.env.user)
  created_by_name = fields.Char(string="Hoạt động được tạo bởi ", store=True, default = lambda self: self.env.user.name)
 
  department_of_create_user = fields.Many2one(related='user_id.manage_department_id', 
  string='Hoat dong thuoc ve don vi', store=True, default=lambda self: self.env.user.manage_department_id)
  
  date_begin_registration = fields.Datetime(string='Ngày bắt đầu đăng ký', required=True, tracking=True)
  date_end_registration = fields.Datetime(string='Ngày kết thúc đăng ký', required=True, tracking=True)
  max_social_point = fields.Char(string="Số ngày CTXH tối đa")
  max_tranning_point = fields.Integer(string="DRL toi da")

  description = fields.Text(string="Nội dung hoạt động", widget="html" )
  attach_file = fields.Many2many('ir.attachment', string='Attachments', widget='many2many_binary')

  is_for_all_students = fields.Boolean(string="Dành cho toàn bộ sinh viên", default=True)
  is_maximize_department = fields.Boolean(string="Giới hạn đơn vị tham gia", default=False)
  is_maximize_major = fields.Boolean(string="Giới hạn chuyên ngành tham gia", default=False)
  is_maximize_year = fields.Boolean(string="Giới hạn khoá tham gia", default=False)
  department_can_register = fields.Many2many('user.info.department', string='Department', default=False)
  major_can_register = fields.Many2many('user.info.major', string='Major')
  year_can_register = fields.Many2many('user.info.year', string='Years')

  auto_accept_activity = fields.Boolean('Tu dong duyet', default=False, readonly=True)
  
  accept_registration = fields.Integer(string='Registration Count', compute='_compute_accept_registration')
  unaccpet_registration = fields.Integer(string='Registration Count', compute='_compute_unaccpet_registration')
  duyet_nhanh = fields.Char(string='Duyet nhanh')
  
  user_current_registed_event = fields.Boolean(string="User hiện tại đã đăng ký", default=False)
  
  def compute_event_registed_button(self):
    for event in self:
      exist_registration = self.env['event.registration'].search([('event_id','=',event.id),('email','=',self.env.user.login)],limit=1)
      if exist_registration:
        event.user_current_registed_event = True
      else:
        event.user_current_registed_event = False
        

  @api.depends('registration_ids')
  def _compute_accept_registration(self):
    for activity in self:
      filtered_registrations = activity.registration_ids.filtered(lambda r: r.state == 'open')
      activity.accept_registration = len(filtered_registrations)
  
  @api.depends('registration_ids')
  def _compute_unaccpet_registration(self):
    for activity in self:
      filtered_registrations = activity.registration_ids.filtered(lambda r: r.state == 'draft')
      activity.unaccpet_registration = len(filtered_registrations)

  @api.onchange('is_for_all_students')
  def check_tickets(self):
    if len(self.event_ticket_ids) != 0 and self.is_for_all_students == True:
       raise ValidationError('Khong the chuyen ve tat ca sinh vien vi dang co gioi han sinh vien')

  @api.model
  def default_get(self, fields_list):
        result = super().default_get(fields_list)
        if 'date_begin_registration' in fields_list and 'date_begin_registration' not in result:
            now = fields.Datetime.now()
            # Round the datetime to the nearest half hour (e.g. 08:17 => 08:30 and 08:37 => 09:00)
            result['date_begin_registration'] = now.replace(second=0, microsecond=0) + timedelta(minutes=-now.minute % 30)
        if 'date_end_registration' in fields_list and 'date_end_registration' not in result and result.get('date_begin_registration'):
            result['date_end_registration'] = result['date_begin_registration'] + timedelta(days=1)
        return result

  @api.model
  def create(self, vals):
    if not vals:
        vals = {}
        
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Before create event: ', vals)
    # Create the record
    if 'auto_accept_activity' in vals and vals['auto_accept_activity'] == True:
      vals['stage_id'] = self.env['event.stage'].search([('name', '=', 'Đã duyệt')]).id
    
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ After create event: ', vals)
    record = super(EventEvent, self).create(vals)
        
    return record
    
  def write(self, vals):
    self.ensure_one()
    # Nay tu dong duyet hoat dong if 'event_type_id' in vals and vals['event_type_id'] == 3:
    #   vals['stage_id'] = 8
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Before update event: ', vals)
    #publish_event_website
    vals['is_published'] = False
    if ('stage_id' not in vals and self.stage_id.name == 'Đã duyệt') or ('stage_id' in vals and self.env['event.stage'].search([('id', '=', vals['stage_id'])]).name == 'Đã duyệt'):
      vals['is_published'] = True  
    
    #change_stage
    print(self.stage_id.name)
    if 'stage_id' not in vals and self.stage_id.name == 'Bổ sung'   :
      vals['stage_id'] = self.env['event.stage'].search([('name', '=', 'Chờ duyệt')]).id
   
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Update event: ', vals)
   
    return super(EventEvent, self).write(vals)

  @api.depends('stage_id', 'date_begin_registration', 'date_end_registration', 'date_begin', 'date_end')
  def _compute_status_activity(self):
        current_datetime = datetime.now()
        for event in self:
            print('^^^^^^^^6', event.stage_id.name)
            if event.stage_id.name == 'Đã duyệt':
                if current_datetime < event.date_begin_registration:
                    event.status_activity = 'new'
                elif event.date_begin_registration <= current_datetime <= event.date_end_registration:
                    event.status_activity = 'open_registration'
                elif event.date_end_registration < current_datetime < event.date_begin:
                    event.status_activity = 'close_registration'
                elif event.date_begin <= current_datetime <= event.date_end:
                    event.status_activity = 'inprogress'
                elif current_datetime > event.date_end:
                    event.status_activity = 'completed'
            else:
                event.status_activity = False

  def see_info(self):
    self.ensure_one()
    return{
        'name': 'Thông tin hoạt động',
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'event.event',
        'view_id': False,
        'res_id': self.id,
        'target': 'current',
    }
        
  def confirm_event(self):
    self.ensure_one()
    stage_id = self.env['event.stage'].search([('name', '=', 'Đã duyệt')]).id
    self.write({'stage_id': stage_id})
    return self.notify_success()

  def need_update_event(self):
    self.ensure_one()
    stage_id = self.env['event.stage'].search([('name', '=', 'Bổ sung')]).id
    self.write({'stage_id': stage_id})
    return self.notify_success()

  def refuse_event(self):
    self.ensure_one()
    stage_id = self.env['event.stage'].search([('name', '=', 'Đã huỷ')]).id
    self.write({'stage_id': stage_id})
    return self.notify_success()
  
  def register_event(self):
    self.ensure_one()
    return{
        'name': 'Thông tin đăng ký hoạt động',
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'event.registration.wizard',
        'view_id': False,
        'target': 'new',
    }
  
  def cancel_event_registration(self):
    self.ensure_one()
    resgistration = self.env['event.registration'].search([('event_id','=',self.id),('email','=',self.env.user.login)],limit=1)
    if resgistration:
      resgistration.sudo().unlink()
      self.compute_event_registed_button()
    return self.notify_success()

  def notify_success(self):
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Thành công',
            'message': 'Thao tác của bạn đã được lưu',
            'type': 'success',
            'sticky': False, 
            'next': {'type': 'ir.actions.act_window_close'},
        },
    }

  @api.constrains('date_begin_registration', 'date_end_registration', 'date_begin', 'date_end')
  def _check_dates(self):
        current_date = datetime.today()
        for activity in self:
            if activity.date_begin_registration >= activity.date_end_registration:
                raise ValidationError('Ngày kết thúc đăng ký phải sau ngày đăng ký')
            if activity.date_begin >= activity.date_end:
                raise ValidationError('Ngày kết thúc phải sau ngày bắt đầu')
            if activity.date_begin_registration >= activity.date_end:
                raise ValidationError('Ngày bắt đầu đăng ký phải trước ngày kết thúc')
            if activity.date_begin < current_date:
              raise ValidationError('Ngày bắt đầu phải từ ngày hôm nay trở đi')
            if activity.date_end < current_date:
              raise ValidationError('Ngày kết thúc phải từ ngày hôm nay trở đi')
            if activity.date_begin_registration < current_date:
              raise ValidationError('Ngày bắt đầu đăng ký phải từ ngày hôm nay trở đi')
            if activity.date_end_registration < current_date:
              raise ValidationError('Ngày kết thúc đăng ký phải từ ngày hôm nay trở đi')

  @api.onchange('is_for_all_students','is_maximize_department')
  def _change_checkbox(self):
    for record in self:
      if record.is_for_all_students == True:
        record.is_maximize_department = False
        record.is_maximize_major = False
        record.is_maximize_year = False
      if record.is_maximize_department == False:
        if record.is_maximize_major == True:
          record.is_maximize_major = False

class ResUsers(models.Model):
  _inherit = ['res.users']

class UserDepartmentAdmin(models.Model):
  _inherit = ['user.department.admin']

class ActivityDepartment(models.Model):
  name = 'activity.department'
  _inherit = 'user.info.department'

  max_num_resgis = fields.Integer('So luong dang ky toi da')

class UserInfoMajor(models.Model):
  _inherit = 'user.info.major'
class UserInfoYear(models.Model):
  _inherit = 'user.info.year'