from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re
from . import common_constants
class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  user_id = fields.Many2one('res.users', string='User', readonly=True, default=lambda self: self.env.uid)
  
  name= fields.Char(related='user_id.name', string="Name")
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(string='Avatar')
  first_name = fields.Char('First Name')
  sur_name = fields.Char('Sur Name')

  
  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')])
  birth_date = fields.Date(string="Birth Day")
  nation = fields.Char(string="Nation")
  personal_email = fields.Char(string="Personal Email")
  religion = fields.Selection(common_constants.RELIGION, string="Religion")

  ethnicity = fields.Selection(common_constants.ETHNICITY, string='Ethnicity')
  national_id = fields.Char(string="National Id")

  date_communist_party= fields.Date(string="Date At Communist Party")
  place_communist_party = fields.Char(string="Place Communist Party")
  date_at_union = fields.Date(string="Date At Union")
  place_union = fields.Char(string="Place Union")
  date_at_student_association = fields.Date(string="Date at Student Association")
  
  native_address = fields.Char(string="Native Address")
  native_address_specific = fields.Char(string="Native Address Specific")
  province_id_native = fields.Many2one('user.province.info', 'Province (Native)', widget='selection')
  district_id_native = fields.Many2one('user.district.info', 'District (Native)', domain="[('province_id', '=', province_id_native)]", widget='selection')
  ward_id_native = fields.Many2one('user.ward.info', 'Ward (Native)', domain="[('district_id', '=', district_id_native)]", widget='selection')
  
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Permanent Address Specific")
  province_id_permanent = fields.Many2one('user.province.info', 'Province (Permanent)', widget='selection')
  district_id_permanent = fields.Many2one('user.district.info', 'District (Permanent)', domain="[('province_id', '=', province_id_permanent)]", widget='selection')
  ward_id_permanent = fields.Many2one('user.ward.info', 'Ward (Permanent)', domain="[('district_id', '=', district_id_permanent)]", widget='selection')

  student_id = fields.Char(string="Student ID")
  user_info_department_id = fields.Many2one('user.info.department',string='Department')
  year_in = fields.Char(string="Year in", compute="_compute_year_in")
  user_info_major_id = fields.Many2one('user.info.major',string='Major')
  user_info_class_id = fields.Many2one('user.info.class',string='Class')

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
  
  def open_list_user_info(self):
    action = {
      'name': 'User Information',
      'type': 'ir.actions.act_window',
      'view_mode': 'tree,form',
      'res_model': 'user.info',  
    }
    if self.env.user.manage_department_id:
      action.update({
        'domain': [('user_info_department_id','=',self.env.user.manage_department_id.id)]
      })
    return action    
   
  @api.depends('name')
  def _compute_name_parts(self):
    for user in self:
      if user.name:
        name_parts = user.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 
  
  @api.onchange('personal_email')
  def _validate_email(self):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if self.personal_email and not re.match(pattern, self.personal_email):
      return {
        'warning': {
        'title': 'Invalid Input',
        'message': 'Invalid Email',
        }
      }

  @api.onchange('student_id')
  def _onchange_number_field(self):
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
  
  @api.depends('student_id')
  def _compute_year_in(self):
    for record in self:
        if record.student_id:
            year_prefix = record.student_id[:2]
            record.year_in = str(int(year_prefix) + 2000)
        else:
          record.year_in=""

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
  
    
class ResUsers(models.Model):
  _inherit = ['res.users']
  
  user_info_id = fields.One2many('user.info', 'user_id', string='User Info')
  manage_department_id = fields.Many2one('user.info.department')
  
  @api.model
  def create(self, vals):
    # department: 15, super: 16, techinical: 17, user:14
    login_email = vals['login']
    pattern = r'^[A-Za-z0-9._%+-]+@hcmut\.edu\.vn$'
    
    group_user_id = self.env['res.groups'].search([('name','=','User')]).id  
    group_department_admin_id = self.env['res.groups'].search([('name','=','Department Admin')]).id
    group_super_admin_id = self.env['res.groups'].search([('name','=','Super Admin')]).id
    
    super_admin = self.env['user.super.admin'].search([('email', '=', login_email)], limit=1)
    department_admin = self.env['user.department.admin'].search([('email', '=', login_email)], limit=1)
    
    if not re.match(pattern, login_email):
      raise ValueError("Invalid email address. Email must end with @hcmut.edu.vn")
    elif super_admin:
      vals.update({
        'groups_id': [(6, 0, [1, group_super_admin_id])],
        'hide_menu_ids': [(6, 0, [73, 5])],
        'lang': 'vi_VN',
        'tz': 'Asia/Ho_Chi_Minh'
      })
    elif department_admin:
      vals.update({
        'groups_id': [(6, 0, [1, group_department_admin_id])],
        'hide_menu_ids': [(6, 0, [73, 5])],
        'lang': 'vi_VN',
        'tz': 'Asia/Ho_Chi_Minh',
        'manage_department_id': department_admin.id
      })
    else:  
      vals.update({
        'groups_id': [(6, 0, [1, group_user_id])],
        'hide_menu_ids': [(6, 0, [73, 5])],
        'lang': 'vi_VN',
        'tz': 'Asia/Ho_Chi_Minh'
      })
    print(vals)
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
          
  
  
  
  
  
  
