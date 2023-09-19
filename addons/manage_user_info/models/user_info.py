from odoo import models, fields,api

class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  def _default_user(self):
    return self.env.uid
  
  user_id = fields.Many2one('res.users', string='User', readonly=True)
  
  name= fields.Char(related='user_id.name', string="Name")
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(related='user_id.image_128', string='Avatar', readonly=True)
  first_name = fields.Char('First Name',compute='_compute_name_parts', store=True)
  sur_name = fields.Char('Sur Name',compute='_compute_name_parts', store=True)

  student_id = fields.Char(string="Student ID")
  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')])
  birth_date = fields.Date(string="Birth Day")
  nation = fields.Char(string="Nation")
  personal_email = fields.Char(string="Personal Email")
  religion = fields.Char(string="Religion")
  national_id = fields.Char(string="National Id")
  
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Permanent Address Specific")
  
  date_communist_party= fields.Date(string="Date At Communist Party")
  place_communist_party = fields.Char(string="Place Communist Party")
  date_at_union = fields.Date(string="Date At Union")
  place_union = fields.Char(string="Place Union")
  date_at_student_association = fields.Date(string="Date at Student Association")
  native_address = fields.Char(string="Native Address")
  native_address_specific = fields.Char(string="Native Address Specific")
  
  province_id = fields.Many2one('user.province.info', 'Province')
  district_id = fields.Many2one('user.district.info', 'District')
  ward_id = fields.Many2one('user.ward.info', 'Ward')
  
  user_info_department_id = fields.Many2one('user.info.department',string='Department')
  user_info_major_id = fields.Many2one('user.info.major',string='Major')
  user_info_class_id = fields.Many2one('user.info.class',string='Class')
   
  @api.depends('name')
  def _compute_name_parts(self):
    for user in self:
      if user.name:
        name_parts = user.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 
  
class ResUsers(models.Model):
  _inherit = ['res.users']
  
  user_info_id = fields.One2many('user.info', 'user_id', string='User Info')

  
  
  
  
  
