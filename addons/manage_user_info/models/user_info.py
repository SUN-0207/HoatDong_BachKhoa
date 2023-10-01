from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re
from . import common_constants
class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  states = fields.Selection(selection=[
       ('draft', 'Draft'),
       ('done', 'Done'),
    ], 
    string='Status', 
    required=True, 
    readonly=True, 
    copy=False,
    tracking=True, 
    default='draft',
  )

  user_id = fields.Many2one('res.users', string='User', readonly=True)
  
  name = fields.Char(related='user_id.name', string="Name", store=True, compute='_compute_name_parts')
  first_name = fields.Char('First Name', inverse='_inverse_name', store=True)
  sur_name = fields.Char('Sur Name', inverse='_inverse_name', store=True)
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(string='Avatar')

  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')])
  birth_date = fields.Date(string="Birth Day")
  nation = fields.Char(string="Nation")
  personal_email = fields.Char(string="Personal Email")
  religion = fields.Selection(common_constants.RELIGION, string="Religion")

  ethnicity = fields.Selection(common_constants.ETHNICITY, string='Ethnicity')
  national_id = fields.Char(string="National Id")
  national_id_date = fields.Date(string="Created date Nation ID")
  national_id_place = fields.Char(string="Created palce Nation ID")

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
  user_info_department_id = fields.Many2one('user.info.department', string='Department', readonly=True, store=True, compute='_compute_user_info_department')
  user_info_major_id = fields.Many2one('user.info.major',string='Major', store=True)
  user_info_class_id = fields.Many2one('user.info.class',string='Class', 
    domain=lambda self: self._compute_user_info_class_domain(),
    store=True
  )
  
  def button_draft(self):
       self.write({
           'states': "draft"
       })
  
  def button_done(self):
       self.write({
           'states': "done"
       })

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
  
  @api.onchange('first_name', 'sur_name')
  def _inverse_name(self):
    for user in self:
        if user.first_name or user.sur_name:
            name_parts = []
            if user.first_name:
                name_parts.append(user.first_name)
            if user.sur_name:
                name_parts.append(user.sur_name)
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

  @api.onchange('personal_email')
  def _validate_email(self):
    pattern = r".*@gmail\.com$"
    if self.personal_email and not re.match(pattern, self.personal_email):
      return {
        'warning': {
        'title': 'Invalid Input',
        'message': 'Invalid Email',
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
  
  @api.onchange('student_id', 'user_info_major_id')
  def _compute_user_info_class_domain(self):
    pattern = r'^0?\d{7}$'
    year = ""
    if self.student_id:
        if not self.student_id.isdigit() or not re.match(pattern, self.student_id):
            return {
                'warning': {
                    'title': 'Invalid Input',
                    'message': 'Invalid student ID. Student ID must be a 7-digit number.',
                }
            }
        year_prefix = self.student_id[:2]
        year = str(int(year_prefix) + 2000)

    domain = []
    if self.user_info_major_id:
        domain = [('major_id', '=', self.user_info_major_id.id)]
    if self.student_id and year != "":
        domain.append(('year', '=', year))

    self.user_info_class_id = False
    return {
        'domain': {'user_info_class_id': domain} if domain else {},
    }

  @api.depends('user_info_major_id', 'student_id')
  def _compute_user_info_department(self):
    for record in self:
        if record.user_info_major_id:
            record.user_info_department_id = record.user_info_major_id.department_id
        else:
            record.user_info_department_id = False
    
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
    
    # if not re.match(pattern, login_email):
    #   raise ValueError("Invalid email address. Email must end with @hcmut.edu.vn")
    if super_admin:
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
          
  
  
  
  
  
  
