from odoo import models, fields, api
import json
import requests

import logging

_logger = logging.getLogger(__name__)

class UserInfoContact(models.Model):
  _name = 'user.info.contact'
  _description = 'User Info Contact'
  # _inherits = ['user.info']

  contact_id = fields.Many2one('user.info', string="User id", ondelete='cascade', delegate=True)

  student_id = fields.Char(string="Student ID", required=True)
  phone_number = fields.Char(string="Phone number", required=True)
  gender = fields.Selection([('male', 'Male'),('female', 'Female')], required=True)
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
  
  province = fields.Selection(
        selection='_get_province_data',
        string='Province',
  )

  district = fields.Selection(
      selection='_get_districts',
      string='District'
  )

  # @api.model
  # def _get_province_data(self):
  #   options = []
  #   response = requests.get("https://provinces.open-api.vn/api/p/")
  #   response.raise_for_status()
  #   data = response.json()

  #   for province_data in data:
  #     options.append((province_data['code'], province_data['name']))

  #   return options
  
  # @api.depends('province')
  # def _get_districts(self):    
  #   if self.province:
  #     options = []
  #     response = requests.get("https://provinces.open-api.vn/api/d/")
  #     response.raise_for_status()
  #     data = response.json()
  #     for districts in data:
  #       if(districts['province_code'] == self.province):
  #         options.append((districts['code'], districts['name']))
      
  #   return options
  
  @api.model
  def _get_province_data(self):
        options = []
        response = requests.get("https://provinces.open-api.vn/api/p/")
        response.raise_for_status()
        data = response.json()

        for province_data in data:
            options.append((province_data['code'], province_data['name']))
        return options

  @api.model
  def _get_districts(self):
    print("outside")
    if self.province:
      print("inside")
      options = []
      response = requests.get(f"https://provinces.open-api.vn/api/d/{self.province}")
      response.raise_for_status()
      data = response.json()
      lst = data['districts']
      for district_data in lst:
        options.append((district_data['code'], district_data['name']))
      return options
    else:
        return []

  @api.onchange('province')
  def _onchange_province(self):
    if self.province:
      self.district = False