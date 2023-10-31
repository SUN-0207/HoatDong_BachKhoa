from odoo import models, fields,api, _, Command
from odoo.exceptions import AccessDenied, ValidationError, UserError
import re
from . import common_constants
class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  states = fields.Selection(selection=[
       ('draft', 'Bản nháp'),
       ('done', 'Hoàn tất'),
    ], 
    string='Status', 
    required=True, 
    readonly=True, 
    copy=False,
    tracking=True, 
    default='draft',
  )

  user_id = fields.Many2one('res.users', string='User',ondelete='cascade', readonly=True)
  
  name = fields.Char(compute='_compute_name_parts', string="Name", store=True)
  first_name = fields.Char('Tên', compute='_compute_name_parts', inverse='_inverse_name', store=True)
  sur_name = fields.Char('Họ và tên lót', compute='_compute_name_parts', inverse='_inverse_name', store=True)
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(string='Ảnh chân dung')

  phone_number = fields.Char(string="Số điện thoại di động")
  gender = fields.Selection([('male', 'Nam'),('female', 'Nữ')],string='Giới tính')
  birth_date = fields.Date(string="Ngày sinh")
  nation = fields.Char(string="Nation")
  personal_email = fields.Char(string="Email cá nhân")
  religion = fields.Many2one('user.religion', string="Tôn giáo")

  ethnicity = fields.Many2one('user.ethnicity', string='Dân tộc')
  national_id = fields.Char(string="Số CMND/CCCD")
  national_id_date = fields.Date(string="Ngày cấp")
  # national_id_place = fields.Selection(selection='_get_national_id_place_options', string='Nơi cấp')
  national_id_place = fields.Many2one('user.national.place', 'Nơi cấp')


  joined_communist_party = fields.Boolean(default=False, string="Đã kết nạp Đảng")
  re_date_communist_party= fields.Date(string="Ngày vào Đảng (dự bị)")
  offical_date_communist_party= fields.Date(string="Ngày vào Đảng (chính thức)")
  place_communist_party = fields.Char(string="Nơi vào Đảng")
  
  joined_union = fields.Boolean(default=False, string="Đã kết nạp Đoàn")
  date_at_union = fields.Date(string="Ngày kết nạp Đoàn")
  place_union = fields.Char(string="Nơi kết nạp Đoàn")
  
  joined_student_association = fields.Boolean(default=False, string="Đã kết nạp Hội")
  date_at_student_association = fields.Date(string="Ngày kết nạp Hội")
  
  native_address = fields.Char(string="Native Address")
  native_address_specific = fields.Char(string="Địa chỉ cụ thể")
  province_id_native = fields.Many2one('user.province.info', 'Tỉnh/Thành phố')
  district_id_native = fields.Many2one('user.district.info', 'Quận/Huyện', domain="[('province_id', '=', province_id_native)]")
  ward_id_native = fields.Many2one('user.ward.info', 'Phường/Xã', domain="[('district_id', '=', district_id_native)]")
  
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Địa chỉ cụ thể")
  province_id_permanent = fields.Many2one('user.province.info', 'Tỉnh/Thành phố')
  district_id_permanent = fields.Many2one('user.district.info', 'Quận/Huyện', domain="[('province_id', '=', province_id_permanent)]")
  ward_id_permanent = fields.Many2one('user.ward.info', 'Phường/Xã', domain="[('district_id', '=', district_id_permanent)]")

  user_info_department_id = fields.Many2one('user.info.department', string='Đơn vị', readonly=True, store=True, compute='_compute_user_info_department')
  user_info_major_id = fields.Many2one('user.info.major',string='Ngành', store=True)
  user_info_academy_year = fields.Many2one('user.info.year', string='Niên khoá', store=True, compute="_compute_user_info_academy_year")
  student_id = fields.Char(string="MSSV")
  user_info_class_id = fields.Many2one('user.info.class',string='Lớp', 
    domain=lambda self: self._compute_user_info_class_domain(),
    store=True
  )


  @api.depends('user_info_major_id')
  def _compute_user_info_department(self):
    for record in self:
        if record.user_info_major_id:
            record.user_info_department_id = record.user_info_major_id.department_id
        else:
            record.user_info_department_id = False

  @api.onchange('student_id', 'user_info_major_id')
  def _compute_user_info_class_domain(self):
    pattern = r'^0?\d{7}$'
    domain = [('is_year_active', '=', True)]
    year = ""
    if self.student_id :
      if not self.student_id.isdigit() or not re.match(pattern, self.student_id):
            raise ValidationError(_('Invalid student ID. Student ID must be a 7-digit number.'))
      year_prefix = self.student_id[:2]
      year = str(int(year_prefix) + 2000)
      if self.user_info_class_id and self.user_info_class_id.year_id.name != year:
        self.user_info_class_id = self.env['user.info.class']
      self.user_info_academy_year = self.env['user.info.year'].search([('name', '=', year)], limit=1)
    if self.user_info_major_id:
        domain.append(('major_id', '=', self.user_info_major_id.id))
    if self.user_info_academy_year:
      if self.user_info_academy_year.is_enable:
        domain.append(('year_id', '=', self.user_info_academy_year.id))
      else:
        domain = [('year_id', '=', 0)]
    
    self.user_info_class_id = False
    return {
        'domain': {'user_info_class_id': domain} if domain else {},
    }

  @api.depends('user_info_class_id', 'student_id')
  def _compute_user_info_academy_year(self):
    for record in self:
      year = ""
      if record.user_info_class_id:
        record.user_info_academy_year = record.user_info_class_id.year_id 
      elif record.student_id :
        year_prefix = record.student_id[:2]
        year = str(int(year_prefix) + 2000)
        if record.user_info_class_id and record.user_info_class_id.year_id.name != year:
          record.user_info_class_id = self.env['user.info.class']
        record.user_info_academy_year = self.env['user.info.year'].search([('name', '=', year)], limit=1)
      else:
        record.user_info_academy_year= False

  def button_draft(self):
    self.write({'states': 'draft'})
  
  def button_done(self):
    self.write({'states': 'done'})

  @api.model
  def create(self, vals):
    vals['states'] = 'draft'
    return super(UserInfo, self).create(vals)

  def write(self, vals):
    if not self.env.user.sudo().has_group('manage_user_info.group_hcmut_department_admin') and self.env.user.id != self.user_id.id:
      print(self.env.user.id)
      print(self.user_id.id)
      raise AccessDenied(_("Bạn không có quyền truy cập vào thông tin này"))
    if 'states' not in vals:
      vals['states'] = 'done'
    return super(UserInfo, self).write(vals)
  
  @api.onchange('avatar')
  def _check_limit_image_size(self):
    # check the file size here before updating the record
    if self.avatar:
      file_size = len(self.avatar)
      if file_size > 5 * 1024 * 1024:
        raise UserError(_('Hình ảnh tải lên không vượt quá 5MB'))

  @api.onchange('phone_number', 'national_id')
  def _validate_number_char_field(self):
        pattern = r'^0?\d{10}$'
        national_id_pattern = r'^\d{9}$|^\d{12}$'
        if self.phone_number and not re.match(pattern, self.phone_number):
            raise ValidationError(_('Invalid phone'))
        if self.national_id and not re.match(national_id_pattern, self.national_id):
            raise ValidationError(_('Invalid nation id'))

  @api.onchange('personal_email')
  def _validate_email(self):
    pattern = r".*@gmail\.com$"
    if self.personal_email and not re.match(pattern, self.personal_email):
      raise ValidationError(_('Invalid personal email'))

  def open_current_user_info(self):
    view_id = self.env.ref('manage_user_info.user_info_view_form') 
    
    current_user_info = self.env['user.info'].search([('user_id', '=', self.env.uid)],limit=1)
    
    if not current_user_info:
      current_user_info = self.env['user.info'].sudo().create({
        'user_id': self.env.uid
      })
      
    return {
        'name': 'Personal Information',
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'user.info',  
        'res_id': current_user_info.id,
        'view_id': view_id.id,
        'target': 'main',
    }
  
  def open_list_user_info(self):
    action = {
      'name': 'Thông tin Sinh viên',
      'type': 'ir.actions.act_window',
      'view_mode': 'tree,form',
      'res_model': 'user.info',  
      'limit': 15,
    }
    if self.env.user.manage_department_id:
      action.update({
        'domain': [('user_info_department_id','=',self.env.user.manage_department_id.id)]
      })
    return action    
  
  def _get_national_id_place_options(self):
    options = [('ccs','Cục Cảnh sát quản lí hành chính về trật tự xã hội')]
    provinces = self.env['user.province.info'].search([])
    for province in provinces:
      options.append((province.codename,province.name))
    return options
   
  @api.depends('user_id.name')
  def _compute_name_parts(self):
    for user in self:
      if user.user_id.name:
        name_parts = user.user_id.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 
        user.name = user.sur_name + " " + user.first_name
  
  def _inverse_name(self):
    for user in self:
        if user.first_name or user.sur_name:
            name_parts = []
            if user.sur_name:
                name_parts.append(user.sur_name)
            if user.first_name:
                name_parts.append(user.first_name)
            user.name = " ".join(name_parts)
        else:
            user.name = False
  
  @api.onchange('province_id_native')
  def on_province_native_change(self):
    if self.province_id_native:
      self.district_id_native = False
      self.ward_id_native = False
  
  @api.onchange('district_id_native')
  def on_district_native_change(self):
    if self.district_id_native:
      self.ward_id_native = False
  
  @api.onchange('province_id_permanent')
  def on_province_permanent_change(self):
    if self.province_id_permanent:
      self.district_id_permanent = False
      self.ward_id_permanent= False
  
  @api.onchange('district_id_permanent')
  def on_district_permanent_change(self):
    if self.district_id_permanent:
      self.ward_id_native = False
   
class ResUsers(models.Model):
  _inherit = ['res.users']
  
  user_info_id = fields.One2many('user.info', 'user_id', string='User Info')
  manage_department_id = fields.Many2one('user.info.department')
  
  @api.model
  def create(self, vals):
    login_email = vals['login']
    pattern = r'^[A-Za-z0-9._%+-]+@hcmut\.edu\.vn$'
    # print(login_email)
    
    # # Group ID
    # group_user_id = self.env['res.groups'].sudo().search([('name','=','User')], limit=1).id
    group_department_admin_id = self.env['res.groups'].sudo().search([('name','=','Department Admin')], limit=1).id
    group_super_admin_id = self.env['res.groups'].sudo().search([('name','=','Super Admin')], limit=1).id
    
    # # Role Admin
    super_admin = self.env['user.super.admin'].search([('email', '=', login_email)], limit=1)
    department_admin = self.env['user.department.admin'].search([('email', '=', login_email)], limit=1)
    if department_admin:
      vals.update({
        'groups_id': [(6, 0, [group_department_admin_id])],
        'manage_department_id': department_admin.department_id.id
      }) 
    elif super_admin:
      vals.update({
        'groups_id': [(6, 0, [group_super_admin_id])],
      })
    elif not re.match(pattern, login_email):
        raise AccessDenied(_("Đăng nhập với tài khoản email đuôi là @hcmut.edu.vn"))
    
    # # Menu ID
    # discuss_id = self.env.ref('mail.menu_root_discuss').id
    # link_tracker_id = self.env.ref('utm.menu_link_tracker_root').id
    # app_id = self.env.ref('base.menu_management').id
    
    # print('kaka')
    # if super_admin:
    #   vals.update({
    #     'groups_id': [(6, 0, [group_super_admin_id])],
    #     'hide_menu_ids': [(6, 0, [discuss_id, link_tracker_id, app_id])],
    #     'lang': 'vi_VN',
    #     'tz': 'Asia/Ho_Chi_Minh'
    #   })
    # elif department_admin:
    #   vals.update({
    #     'groups_id': [(6, 0, [group_department_admin_id])],
    #     'hide_menu_ids': [(6, 0, [discuss_id, link_tracker_id, app_id])],
    #     'lang': 'vi_VN',
    #     'tz': 'Asia/Ho_Chi_Minh',
    #     'manage_department_id': department_admin.department_id.id
    #   })
    # else:  
    #   if not re.match(pattern, login_email):
    #     raise AccessDenied(_("Đăng nhập với tài khoản email đuôi là @hcmut.edu.vn"))
    #   vals.update({
    #     'groups_id': [(6, 0, [group_user_id])],
    #     'hide_menu_ids': [(6, 0, [discuss_id, link_tracker_id, app_id])],
    #     'lang': 'vi_VN',
    #     'tz': 'Asia/Ho_Chi_Minh'
    #   })
    print('===================================')
    print('Create')
    print(vals)
    print('===================================')
    return super(ResUsers, self).create(vals)

  def write(self, vals):
    res = super(ResUsers, self).write(vals)
    # email_pattern = r'^[A-Za-z0-9._%+-]+@hcmut\.edu\.vn$'
    # print(self.login)
    # super_admin = self.env['user.super.admin'].sudo().search([('email', '=', self.login)], limit=1)
    # department_admin = self.env['user.department.admin'].sudo().search([('email', '=', self.login)], limit=1)
    # if not super_admin and not department_admin and not re.match(email_pattern,self.login) and self.login != 'admin' and self.login != 'default':
    #   raise AccessDenied(_("Đăng nhập với tài khoản email đuôi là @hcmut.edu.vn"))
    print('===================================')
    print('Update')
    print(vals)
    print('===================================')
    
    for user in self:
      for menu in user.hide_menu_ids:
          menu.write({
              'restrict_user_ids': [(4, user.id)]
          })
    return res
  
  def unlink(self):
    for user in self:
      if user.user_info_id:
        user.user_info_id.unlink()
    return super(ResUsers,self).unlink()

  def _get_is_admin(self):
      for rec in self:
          rec.is_admin = False
          if rec.id == self.env.ref('base.user_admin').id:
              rec.is_admin = True

  hide_menu_ids = fields.Many2many('ir.ui.menu', string="Menu", store=True)
  is_admin = fields.Boolean(compute=_get_is_admin)

class RestrictMenu(models.Model):
    _inherit = 'ir.ui.menu'

    restrict_user_ids = fields.Many2many('res.users')
    
class OAuthConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def get_values(self):
      res = super(OAuthConfigSettings, self).get_values()
      client_id = "851307936783-vd6m4djqivgrt3kimt70hu5f9323amgd.apps.googleusercontent.com"
      lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', 'vi_VN')], limit=1)
      if not lang['active']:
          installer = self.env['base.language.install'].create({
              'lang_ids': [(4, lang.id)] 
          })
          installer.lang_install()
      if not res['auth_oauth_google_enabled'] and res['auth_oauth_google_client_id'] != client_id:
        res.update({
            'auth_oauth_google_enabled': True,
            'auth_oauth_google_client_id': client_id,
        })
      oauth_provider = self.env['auth.oauth.provider'].search([('name', '=', 'Google OAuth2')], limit=1)
      odoo_provider = self.env['auth.oauth.provider'].search([('name', '=', 'Odoo.com Accounts')], limit=1)
      if oauth_provider['client_id'] != client_id and not oauth_provider['enabled']:
        oauth_provider.update({
            'client_id': client_id,
            'enabled': True,
        })
      if odoo_provider['enabled']:
        odoo_provider.update({
            'enabled': False,
        })
      return res
          
  
  
  
  
  
  
