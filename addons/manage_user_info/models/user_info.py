from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re
from . import common_constants
class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  user_id = fields.Many2one('res.users', string='User', readonly=True)
  
  name = fields.Char(related='user_id.name', string="Name", store=True)
  first_name = fields.Char('First Name', compute='_compute_name_parts', inverse='_inverse_name')
  sur_name = fields.Char('Sur Name', compute='_compute_name_parts', inverse='_inverse_name')
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(string='Avatar')

  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')])
  birth_date = fields.Date(string="Birth Day")
  nation = fields.Char(string="Nation")
  personal_email = fields.Char(string="Personal Email")
  religion = fields.Selection(common_constants.RELIGION, string="Religion", translate=False)
  ethnicity = fields.Selection(common_constants.ETHNICITY, string='Ethnicity', translate=False)

  date_communist_party= fields.Date(string="Date At Communist Party")
  place_communist_party = fields.Char(string="Place Communist Party")
  date_at_union = fields.Date(string="Date At Union")
  place_union = fields.Char(string="Place Union")
  date_at_student_association = fields.Date(string="Date at Student Association")
  
  national_id = fields.Char(string="National Id")
  national = fields.Selection(common_constants.NATIONAL,string="National", translate=False)
  
  native_address = fields.Char(string="Native Address")
  native_address_specific = fields.Char(string="Native Address Specific")
  province_id_native = fields.Many2one('user.province.info', string='Province')
  district_id_native = fields.Many2one('user.district.info', string='District', domain="[('province_id', '=', province_id_native)]")
  ward_id_native = fields.Many2one('user.ward.info', string='Ward', domain="[('district_id', '=', district_id_native)]")
  
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Permanent Address Specific")
  province_id_permanent = fields.Many2one('user.province.info', string='Province')
  district_id_permanent = fields.Many2one('user.district.info', string='District', domain="[('province_id', '=', province_id_permanent)]")
  ward_id_permanent = fields.Many2one('user.ward.info', string='Ward', domain="[('district_id', '=', district_id_permanent)]")

  student_id = fields.Char(string="Student ID")
  falcutian_id = fields.Char(string="Falcutian ID")

  user_info_department_id = fields.Many2one('user.info.department',string='Department')
  year_in = fields.Char(string="Year in", compute="_compute_year_in", store=True)
  user_info_major_id = fields.Many2one('user.info.major',string='Major')
  user_info_class_id = fields.Many2one('user.info.class',string='Class', translate=False)

  personal_email_valid = fields.Boolean(string='Invalid Email',default=True)
  
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
        'target': 'current',
    }
   
  @api.depends('name')
  def _compute_name_parts(self):
    for record in self:
        if record.name:
            name_parts = record.name.split(" ")
            record.first_name = name_parts[0] if name_parts else ''
            record.sur_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ''
        else:
            record.first_name = ''
            record.sur_name = ''

  def _inverse_name(self):
    for record in self:
        record.name = record.first_name + ' ' + record.sur_name if record.first_name or record.sur_name else ''

  @api.onchange('national')
  def on_national_change(self):
    if self.national != '2':
      self.province_id_native = False
      self.district_id_native = False
      self.ward_id_native = False

  @api.onchange('province_id_native')
  def on_province_native_change(self):
    if self.province_id_native:
      self.district_id_native = False
      self.ward_id_native = False
  
  @api.onchange('self.district_id_native')
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

  @api.onchange('user_info_department_id')
  def on_department_change(self):
    if self.user_info_department_id:
      self.user_info_major_id = False
      self.user_info_class_id = False
  
  @api.onchange('user_info_major_id')
  def on_major_change(self):
    if self.user_info_major_id:
      self.user_info_class_id = False

  @api.onchange('personal_email')
  def on_personal_email_change(self):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if self.personal_email and not re.match(pattern, self.personal_email):
      return {
        'warning': {
        'title': 'Invalid Input',
        'message': 'Invalid Email',
        }
      }

  @api.onchange('student_id')
  def on_student_id_change(self):
    pattern = r'^0?\d{7}$'
    if self.student_id and not self.student_id.isdigit():
      return {
        'warning': {
        'title': 'Invalid Input',
        'message': 'Only numbers are allowed in the Number Field.',
        }
      }
    if self.student_id and not re.match(pattern, self.student_id):
      return {
        'warning': {
        'title': 'Invalid Input',
        'message': 'Invalid student ID. Student ID must be a 7-digit number.'
        }
      }
  
  @api.onchange('phone_number')
  def _onchange_phone_field(self):
    pattern = r'^0?\d{10}$'
    if self.phone_number and not re.match(pattern, self.phone_number):
      return {
        'warning': {
        'title': 'Invalid Input',
        'message': 'Invalid phone number'
        }
      }

  @api.depends('student_id')
  def _compute_year_in(self):
    for record in self:
        if record.student_id:
            year_prefix = record.student_id[:2]
            record.year_in = str(int(year_prefix) + 2000)
        else:
          record.year_in=""

  
    
class ResUsers(models.Model):
  _inherit = ['res.users']
  
  user_info_id = fields.One2many('user.info', 'user_id', string='User Info')
  
  @api.model
  def create(self, vals):
    vals.update({
      'groups_id': [(6, 0, [1, 13, 7, 14])],
      'hide_menu_ids': [(6, 0, [73, 5])],
      'lang': 'vi_VN',
      'tz': 'Asia/Ho_Chi_Minh'
    })
    return super(ResUsers, self).create(vals)

  def write(self, vals):
    res = super(ResUsers, self).write(vals)
    for menu in self.hide_menu_ids:
        menu.write({
            'restrict_user_ids': [(4, self.id)]
        })
    return res

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
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', 'vi_VN')], limit=1)
        if lang:
            installer = self.env['base.language.install'].create({
                'lang_ids': [(4, lang.id)] 
            })
            installer.lang_install()
        res.update({
            'auth_oauth_google_enabled': True,
            'auth_oauth_google_client_id': "57505462055-ehit1cdp8rji767v6gdmd5r0bl5dpcaa.apps.googleusercontent.com",
        })
        oauth_provider = self.env['auth.oauth.provider'].search([('name', '=', 'Google OAuth2')], limit=1)
        odoo_provider = self.env['auth.oauth.provider'].search([('name', '=', 'Odoo.com Accounts')], limit=1)
        oauth_provider.update({
            'client_id': "57505462055-ehit1cdp8rji767v6gdmd5r0bl5dpcaa.apps.googleusercontent.com",
            'enabled': True,
        })
        odoo_provider.update({
            'enabled': False,
        })
        return res
          
  
  
  
  
  
  
