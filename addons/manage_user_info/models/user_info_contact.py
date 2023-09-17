from odoo import models, fields, api
import requests
import re
from odoo.exceptions import ValidationError


class UserInfoContact(models.Model):
  _name = 'user.info.contact'
  _description = 'User Info Contact'
  
  student_id = fields.Char(string="Student ID", required=True)
  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')], required=True)
  birth_date = fields.Date(string="Birth Day", required=True)
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

  @api.constrains('student_id')
  def _validate_name(self):
    pattern = r'^0?\d{6}$'
    for record in self:
      if not re.match(pattern, record.student_id):
        raise ValidationError("Invalid student ID.")

      