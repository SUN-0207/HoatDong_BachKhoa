from odoo import models, fields,api

class UserInfo(models.Model):
  _name = 'user.info'

  _description = 'User Info'

  first_name = fields.Char('Firts Name',compute='_compute_name_parts', store=True)
  sur_name = fields.Char('Sur Name',compute='_compute_name_parts', store=True)
  user_id = fields.Many2one('res.users',string="User", required=True, ondelete='cascade', delegate=True)
  # user_info_major_id = fields.Many2one('user.info.major',string='Major', required=True, ondelete='cascade')
  # user_info_department_id = fields.Many2one('user.info.department',string='Department', required=True, ondelete='cascade')
  # user_info_contact_id = fields.One2Many('user.info.contact','contact_id', required=True, ondelete='cascade')
  # user_info_class_id = fields.Many2one('user.info.class',string='Class', required=True, ondelete='cascade')
  
  student_id = fields.Char(string="Student ID", required=True)
  phone_number = fields.Char(string="Phone number", required=True)
  gender = fields.Char(string="Gender", required=True)
  birth_date = fields.Char(string="Birth Day", required=True)
  nation = fields.Char(string="Nation")
  personal_email = fields.Char(string="Personal Email", required=True)
  religion = fields.Char(string="Religion")
  national_id = fields.Char(string="National Id", required=True)
  native_address = fields.Char(string="Native Address")
  native_address_specific = fields.Char(string="Native Address Specific")
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Permanent Address Specific")
  place_union = fields.Char(string="Place Union")
  date_at_union = fields.Char(string="Date At Union")
  place_communist_party = fields.Char(string="Place Communist Party")
  date_at_student_association = fields.Char(string="Date at Student Association")

  @api.depends('name')
  def _compute_name_parts(self):
    for user in self:
      if user.name:
        name_parts = user.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 

  
  
