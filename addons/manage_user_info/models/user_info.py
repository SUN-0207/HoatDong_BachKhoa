from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re
from . import common_constants
class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  def _default_user(self):
    return self.env.uid
  
  user_id = fields.Many2one('res.users', string='User', readonly=True)
  
  name= fields.Char(related='user_id.name', string="Name")
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(string='Avatar')
  first_name = fields.Char('First Name',compute='_compute_name_parts', store=True)
  sur_name = fields.Char('Sur Name',compute='_compute_name_parts', store=True)

  
  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')], required=True)
  birth_date = fields.Date(string="Birth Day")
  nation = fields.Char(string="Nation", translate=True)
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
  province_id_native = fields.Many2one('user.province.info', 'Province')
  district_id_native = fields.Many2one('user.district.info', 'District', domain="[('province_id', '=', province_id_native)]")
  ward_id_native = fields.Many2one('user.ward.info', 'Ward', domain="[('district_id', '=', district_id_native)]")
  
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Permanent Address Specific")
  province_id_permanent = fields.Many2one('user.province.info', 'Province')
  district_id_permanent = fields.Many2one('user.district.info', 'District', domain="[('province_id', '=', province_id_permanent)]")
  ward_id_permanent = fields.Many2one('user.ward.info', 'Ward', domain="[('district_id', '=', district_id_permanent)]")

  # role = fields.Selection([('admin','Admin'),('student', 'Student'), ('teacher', 'Teacher')], string='Role')
  # teacher_id = fields.Char(string="Teacher ID")

  student_id = fields.Char(string="Student ID")
  user_info_department_id = fields.Many2one('user.info.department',string='Department')
  user_info_major_id = fields.Many2one('user.info.major',string='Major')
  user_info_class_id = fields.Many2one('user.info.class',string='Class')

  
  def open_current_user_info(self):
    view_id = self.env.ref('manage_user_info.user_info_view_form') 
    
    current_user_info = self.env['user.info'].search([('user_id', '=', self.env.uid)],limit=1)
    
    if not current_user_info:
      current_user_info = self.env['user.info'].create({
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
          'message': 'Invalid email address!',
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
        'message': 'Invalid student ID. Student ID must be a 7-digit number.',
        }
      }
    
class ResUsers(models.Model):
  _inherit = ['res.users']
  
  user_info_id = fields.One2many('user.info', 'user_id', string='User Info')


  
  
  
  
  
