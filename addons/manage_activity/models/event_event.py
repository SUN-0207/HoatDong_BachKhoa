from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
class EventEvent(models.Model):
  _name = 'event.event'
  _inherit = [
        'event.event'
    ]

  name = fields.Char(string='Tên hoạt động', translate=False, required=True)
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
  
  user_response = fields.Many2one('user.info', domain=[('can_response_event', '=', True)])
  user_response_phone = fields.Char(string="Số điện thoại di động", compute='_get_info', store=True)
  user_response_email = fields.Char(string="Mail", compute='_get_info', store=True)

  @api.depends('user_response')
  def _get_info(self):
      for record in self:
          if record.user_response:
              record.user_response_phone = record.user_response.phone_number
              record.user_response_email = record.user_response.user_id.email
          else:
              record.user_response_phone = False
              record.user_response_email = False


  date_begin_registration = fields.Datetime(string='Ngày bắt đầu đăng ký', required=True, tracking=True)
  date_end_registration = fields.Datetime(string='Ngày kết thúc đăng ký', required=True, tracking=True)
  max_social_point = fields.Char(string="Số ngày CTXH tối đa")
  max_tranning_point = fields.Integer(string="ĐRL tối đa")

  description = fields.Text(string="Mô tả hoạt động", widget="html" )
  attach_file = fields.Many2many('ir.attachment', string='Attachments', widget='many2many_binary')

  is_for_all_students = fields.Boolean(string="Dành cho toàn bộ sinh viên", default=True)
  is_maximize_department = fields.Boolean(string="Giới hạn đơn vị tham gia", default=False)
  is_maximize_major = fields.Boolean(string="Giới hạn chuyên ngành tham gia", default=False)
  is_maximize_year = fields.Boolean(string="Giới hạn khoá tham gia", default=False)
  department_can_register = fields.Many2many('user.info.department', string='Department', default=False)
  major_can_register = fields.Many2many('user.info.major', string='Major')
  year_can_register = fields.Many2many('user.info.year', string='Years')

  auto_accept_activity = fields.Boolean('Tu dong duyet', readonly=True, store=True, compute='_check_auto_accept_activity')
  
  accept_registration = fields.Integer(string='Registration Count', compute='_compute_accept_registration')
  unaccpet_registration = fields.Integer(string='Registration Count', compute='_compute_unaccpet_registration')
  duyet_nhanh = fields.Char(string='Duyet nhanh')

  @api.depends('event_type_id')
  def _check_auto_accept_activity(self):
    for record in self:
      print(record.event_type_id)
      print(record.event_type_id.auto_accept_activity)
      if record.event_type_id :
        record.auto_accept_activity = record.event_type_id.auto_accept_activity

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

  def _validation_ticket_services(self, vals):
    all_students = self.env['user.info.department'].search([('name', '=', 'Tat ca')]).id
    all_students_major = self.env['user.info.major'].search([('name', '=', 'Tat ca')]).id 
    all_students_year = self.env['user.info.year'].search([('name', '=', 'Tat ca')]).id
    is_for_all_school_students = False

    #Auto gen default ticket is "Tat ca" if not choose
    if not self.event_ticket_ids and 'event_ticket_ids' not in vals:
      vals['event_ticket_ids'] = [(0, 0, {'event_department_id': all_students, 'event_info_major_id': all_students_major, 'event_info_academy_year': all_students_year})]
      return
  
    ticket_new = []
    ticket_update = []
    ticket_deleted = []
    ticket_existed = []
    if 'event_ticket_ids' in vals:
      for ticket_id in vals['event_ticket_ids']:
        if ticket_id[0] == 0: 
          if ticket_id[2]['event_info_major_id'] == False:
            ticket_id[2]['event_info_major_id'] = all_students_major
          if ticket_id[2]['event_info_academy_year'] == False:
            ticket_id[2]['event_info_academy_year'] = all_students_year
          ticket_new.append(ticket_id)
        if ticket_id[0] == 1: ticket_update.append(ticket_id)
        if ticket_id[0] == 2: ticket_deleted.append(ticket_id)
        if ticket_id[0] == 4: ticket_existed.append(ticket_id[1])
     
      if len(self.event_ticket_ids) == len(ticket_deleted) and not ticket_new and not ticket_update :
        vals['event_ticket_ids'] += [(0, 0, {'event_department_id': all_students, 'event_info_major_id': all_students_major, 'event_info_academy_year': all_students_year})]
        return
    
    
    # assgin False value to 'Tat ca' for create/update value
      for ticket_id in vals['event_ticket_ids']:
        if ticket_id[0] == 0 :       
          if ticket_id[2]['event_info_major_id'] == False:
            ticket_id[2]['event_info_major_id'] = all_students_major
          if ticket_id[2]['event_info_academy_year'] == False:
            ticket_id[2]['event_info_academy_year'] = all_students_year
        if ticket_id[0] == 1:
          exist_info = self.env['event.event.ticket'].search([('id', '=', ticket_id[1])])
          if 'event_department_id' in ticket_id[2] and  ('event_info_major_id' not in ticket_id[2] or ticket_id[2]['event_info_major_id'] == False ):
              year = self.env['event.event.ticket'].search([('id', '=', ticket_id[1])]).event_info_academy_year
              ticket_id[2].update({'event_info_major_id': all_students_major})
              ticket_id[2].update({'event_info_academy_year': year.id})
          elif 'event_department_id' in ticket_id[2] and ('event_info_academy_year' not in ticket_id[2] or ticket_id[2]['event_info_academy_year'] == False):
              ticket_id[2].update({'event_info_academy_year': all_students_year})
          elif 'event_department_id' not in ticket_id[2] and 'event_info_major_id' in ticket_id[2]:
              major_id =  ticket_id[2]['event_info_major_id']
              if major_id == all_students_major:
                ticket_id[2].update({'event_department_id': exist_info.event_department_id.id})
              else:
                department_id = self.env['user.info.major'].search([('id', '=', major_id)]).department_id
                ticket_id[2].update({'event_department_id': department_id.id})
              if 'event_info_academy_year' not in ticket_id[2]:
                ticket_id[2].update({'event_info_academy_year': exist_info.event_info_academy_year.id})
          elif 'event_info_academy_year' in ticket_id[2] and 'event_department_id' not in ticket_id[2] and 'event_info_major_id' not in ticket_id[2]:
              ticket_id[2].update({'event_department_id': exist_info.event_department_id.id})
              ticket_id[2].update({'event_info_major_id': exist_info.event_info_major_id.id})

    print(ticket_new)
    print(ticket_update)
    print(ticket_deleted)
    print(ticket_existed)

    exist_ticket_info = []
    # Get the exist info of ticket 
    for exist in ticket_existed:
      temp = self.env['event.event.ticket'].browse(exist)[0]
      if temp.event_department_id.display_name  == 'Tat ca':
        is_for_all_school_students = True
      exist_ticket_info.append([temp.id, temp.event_department_id.id, temp.event_info_major_id.id, temp.event_info_academy_year.id]) 
    
    if(ticket_new and not ticket_existed):
      for temp in ticket_new:
        department = self.env['user.info.department'].search([('id', '=', temp[2]['event_department_id'])])
        if department.display_name == 'Tat ca' and  len(ticket_new) > 1:
          raise ValidationError('Không thể thêm lựa chọn tất cả sinh viên toàn trường vì đang có giới hạn đơn vị tham gia. Vui lòng kiểm tra lại ')
    elif (ticket_new and not is_for_all_school_students):
        for temp in ticket_new:
          department = self.env['user.info.department'].search([('id', '=', temp[2]['event_department_id'])])
          if department.display_name == 'Tat ca': 
            raise ValidationError('Không thể thêm lựa chọn tất cả sinh viên toàn trường vì đang có giới hạn đơn vị tham gia. Vui lòng kiểm tra lại ')
    elif ticket_new and is_for_all_school_students:
        raise ValidationError('Đã giới hạn sinh viên toàn trường không thể tạo thêm giới hạn đơn vị. Vui lòng kiểm tra lại ')

    #validate update with exist 
    for update in ticket_update:
      check_all = False
      year_all = False
      for exist in exist_ticket_info:
        if exist[1] == update[2]['event_department_id'] and exist[2] == update[2]['event_info_major_id']:
          if exist[3] == update[2]['event_info_academy_year']:
            raise ValidationError('Khong the cap nhat vi lua chon dang bi trung lap ')
          elif exist[3] == all_students_year or  update[2]['event_info_academy_year'] == all_students_year:
            raise ValidationError('Khong the cap nhat nam vi da co lua chon tat ca ')
        if exist[1] == update[2]['event_department_id']:
          if update[2]['event_info_major_id'] == all_students_major: check_all = True
        if exist[1] == update[2]['event_department_id']:
          if update[2]['event_info_academy_year'] == all_students_major: year_all = True
        if exist[0] != update[1] and check_all:
          raise ValidationError('Không thể cap nhat lựa chọn tất cả sinh viên toàn nganh vì đang có giới hạn nganh tham gia. Vui lòng kiểm tra lại ')
        if exist[0] != update[1] and year_all:
          raise ValidationError('Không thể cap nhat lựa chọn tất cả cac khoa vi đang có giới hạn khoa tham gia. Vui lòng kiểm tra lại ')
        if update[2]['event_department_id'] == all_students and exist[1] != all_students:
          raise ValidationError('Không thể cap nhat lựa chọn tất cả cac don vi vi đang có giới hạn don vi tham gia. Vui lòng kiểm tra lại ')

    for create in ticket_new:
      for exist in exist_ticket_info:
        if exist[1] == create[2]['event_department_id'] and exist[2] == create[2]['event_info_major_id']:
          if exist[3] == create[2]['event_info_academy_year']:
            raise ValidationError('Khong the them vi lua chon dang bi trung lap ')
          elif exist[3] == all_students_year or  create[2]['event_info_academy_year'] == all_students_year:
            raise ValidationError('Khong the them vi da co lua chon tat ca cho khoa')
        elif exist[1] == create[2]['event_department_id'] and exist[2] != create[2]['event_info_major_id']:
          if exist[2] == all_students_major and create[2]['event_info_major_id'] != all_students_major:
            raise ValidationError('Khong the them dieu kien cho nganh vi da chon tat ca nganh cua khoa')
          if exist[2] != all_students_major and create[2]['event_info_major_id'] == all_students_major:
            raise ValidationError('Khong the them dieu kien tat ca nganh vi da co nganh dang duoc gioi han')
      for update in ticket_update:
        if update[2]['event_department_id'] == create[2]['event_department_id'] and update[2]['event_info_major_id'] == create[2]['event_info_major_id']:
          if update[2]['event_info_academy_year'] == create[2]['event_info_academy_year']:
            raise ValidationError('Khong the them vi lua chon dang bi trung lap ')
          elif update[2]['event_info_academy_year'] == all_students_year or  create[2]['event_info_academy_year'] == all_students_year:
            raise ValidationError('Khong the them vi da co lua chon tat ca cho khoa')
        elif update[2]['event_department_id'] == create[2]['event_department_id'] and update[2]['event_info_major_id']!= create[2]['event_info_major_id']:
          if update[2]['event_info_major_id'] == all_students_major and create[2]['event_info_major_id'] != all_students_major:
            raise ValidationError('Khong the them dieu kien cho nganh vi da chon tat ca nganh cua khoa')
          if update[2]['event_info_major_id'] != all_students_major and create[2]['event_info_major_id'] == all_students_major:
            raise ValidationError('Khong the them dieu kien tat ca nganh vi da co nganh dang duoc gioi han')


  
  @api.model
  def create(self, vals):
    if not vals:
        vals = {}
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Before create event: ', vals)
    self._validation_ticket_services(vals)
    # Create the record
    if 'auto_accept_activity' in vals and vals['auto_accept_activity'] == True:
      vals['stage_id'] = self.env['event.stage'].search([('name', '=', 'Đã duyệt')]).id
    
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ After create event: ', vals)
    record = super(EventEvent, self).create(vals)
        
    return record
    
  def write(self, vals):
    self.ensure_one()
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Before update event: ', vals)  
    self._validation_ticket_services(vals)
  
    #change_stage
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

  def see_info_user_response(self):
    self.ensure_one()
    return {
        'name': self.user_response.name,
        'type': 'ir.actions.act_window',
        'res_model': 'see.info.wizard',
        'view_mode': 'form',
        'view_type': 'form',
        'view_id': self.env.ref('manage_activity.view_form_see_info_wizard').id,
        'target': 'new',
        'context': {
            'default_user_response_phone': self.user_response.phone_number,
            'default_user_response_email': self.user_response.user_id.email,
        },
    }

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
    return self.notify_success('Bạn đã chấp nhận hoạt dộng này')

  def need_update_event(self):
    self.ensure_one()
    stage_id = self.env['event.stage'].search([('name', '=', 'Bổ sung')]).id
    self.write({'stage_id': stage_id})
    return self.notify_success('Đã chuyển sang bổ sung')

  def refuse_event(self):
    self.ensure_one()
    stage_id = self.env['event.stage'].search([('name', '=', 'Đã huỷ')]).id
    self.write({'stage_id': stage_id})
    return self.notify_success('Đã từ chối hoạt động này')
  
  def register_event(self):
    self.ensure_one()
    create_date = fields.Datetime.now()
    exist_resgistration = self.env['event.registration'].search([('event_id','=',self.id),('email','=',self.env.user.login)],limit=1)
    if exist_resgistration:
      raise ValidationError('Sự kiện đã được đăng ký')
    registration = self.env['event.registration'].create({
      'create_date': create_date,
      'event_id': self.id,
      'name': self.env.user.user_info_id.name,
      'email': self.env.user.login,
    })
    if self.auto_confirm:
      registration.sudo().action_confirm()
    return self.notify_success()
  
  def cancel_event_registration(self):
    self.ensure_one()
    resgistration = self.env['event.registration'].search([('event_id','=',self.id),('email','=',self.env.user.login)],limit=1)
    if resgistration:
      resgistration.sudo().unlink()
    return self.notify_success()

  def notify_success(self, mess= None):
    if mess == None: 
      mess = 'Thao tác của bạn đã được lưu'
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Thành công',
            'message': mess,
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


class SeeInfoWizard(models.TransientModel):
    _name = 'see.info.wizard'
    _description = 'See Info Wizard'

    user_response_phone = fields.Char(string="Số điện thoại di động", readonly=True)
    user_response_email = fields.Char(string="Mail", readonly=True)

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

class UserInfo(models.Model):
  _inherit = 'user.info'