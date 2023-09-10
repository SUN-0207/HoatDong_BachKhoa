from odoo import models, fields, api
import json
import requests
import re
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

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


  _sql_constraints = [
    ('unique_student_id','UNIQUE (student_id)', 'Student ID must be unique!')
    ]

  @api.constrains('student_id')
  def _validate_name(self):
    pattern = r'^0?\d{7}$'
    for record in self:
      if not re.match(pattern, record.student_id):
        raise ValidationError("Invalid student ID.")

  province = fields.Selection(
        selection='_get_province_data',
        string='Province',
  )
  district = fields.Selection(
      selection=[],
      string='District'
  )

  @api.model
  def _get_province_data(self):
        options = []
        response = requests.get("https://provinces.open-api.vn/api/p/")
        response.raise_for_status()
        data = response.json()

        for province_data in data:
            options.append((province_data['code'], province_data['name']))
        return options

  @api.onchange('province')
  def _onchange_province(self):
    if self.province:
      self.district = []

      response = requests.get("https://provinces.open-api.vn/api/d")
      response.raise_for_status()
      data = response.json()
      _logger.info(data)
      _logger.info(self.province)
      for district_data in data:
        if(district_data['province_code'] == self.province):
          self.district.append((district_data['code'], district_data['name']))

