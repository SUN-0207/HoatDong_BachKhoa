import requests
from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class UserProvinceInfo(models.Model):
  _name = 'user.province.info'
  _description = 'User Province Info'
  
  name = fields.Char('Name', required=True)
  code = fields.Integer('Code', required=True)
  division_type = fields.Char('Division Type')
  codename = fields.Char('Codename')
  phone_code = fields.Integer('Phone Code')
  districts = fields.One2many('user.district.info', 'province_id', 'Districts')
  
class UserDistrictInfo(models.Model):
  _name = 'user.district.info'
  _description = 'User District Info'
  
  name = fields.Char('Name', required=True)
  code = fields.Integer('Code', required=True)
  division_type = fields.Char('Division Type')
  codename = fields.Char('Codename')
  province_id = fields.Many2one('user.province.info', 'Province')
  wards = fields.One2many('user.ward.info', 'district_id', 'Wards')

class UserWardInfo(models.Model):
  _name = 'user.ward.info'
  _description = 'User Ward Info'
  
  name = fields.Char('Name', required=True)
  code = fields.Integer('Code', required=True)
  division_type = fields.Char('Division Type')
  codename = fields.Char('Codename')
  district_id = fields.Many2one('user.district.info', 'District')
  
  @api.model
  def import_location_data(self):
    _logger.info("Starting import_location_data function")
    response = requests.get("https://provinces.open-api.vn/api/p/")
    response.raise_for_status()
    province_datas = response.json()
    
    for province_data in province_datas:
      response = requests.get(f"https://provinces.open-api.vn/api/p/{province_data['code']}?depth=3")
      response.raise_for_status()
      data = response.json()
      
      province_code = province_data['code']
      existing_province = self.env['user.province.info'].search([('code', '=', province_code)], limit=1)
      
      if not existing_province:      
        # Create Province
        province = self.env['user.province.info'].create({
            'name': province_data['name'],
            'code': province_data['code'],
            'division_type': province_data['division_type'],
            'codename': province_data['codename'],
            'phone_code': province_data['phone_code'],
        })
        
        # Create Districts
        for district_data in data['districts']:
            district = self.env['user.district.info'].create({
                'name': district_data['name'],
                'code': district_data['code'],
                'division_type': district_data['division_type'],
                'codename': district_data['codename'],
                'province_id': province.id,
            })

            # Create Wards
            for ward_data in district_data['wards']:
                self.env['user.ward.info'].create({
                    'name': ward_data['name'],
                    'code': ward_data['code'],
                    'division_type': ward_data['division_type'],
                    'codename': ward_data['codename'],
                    'district_id': district.id,
                })
    
    _logger.info("Finished import_location_data function")

# Noi cap CCCD/CMND
class UserNationalPlace(models.Model):
  _name = 'user.national.place'
  _description = 'User National Info Registration Place'
  
  name = fields.Char('Name', required=True)
  codename = fields.Char('Codename', required=True)

  @api.model
  def init(self):
    response = requests.get("https://provinces.open-api.vn/api/p/")
    response.raise_for_status()
    province_datas = response.json()
    
    province_datas.append({'name': 'Cục Cảnh sát quản lí hành chính về trật tự xã hội', 'codename':'ccs'})
    
    for province_data in province_datas:
      codename = province_data['codename']
      existing_province = self.env['user.national.place'].search([('codename', '=', codename)], limit=1)
      
      if not existing_province:      
        province = self.env['user.national.place'].create({
            'name': province_data['name'],
            'codename': province_data['codename'],
        })

  # @api.model
  # def init(self):
  #   national_places = []
  #   national_places.append({'name': 'Cục Cảnh sát quản lí hành chính về trật tự xã hội', 'codename':'ccs'})

  #   provinces = self.env['user.province.info'].search([])
  #   for province in provinces:
  #     national_places.append({'name': province['name'], 'codename': province['codename']})

  #   for place in national_places:
  #     codename = place['codename']
  #     existing_place = self.env['user.national.place'].search([('codename', '=', codename)], limit=1)
  #     if not existing_place:
  #       try:
  #         self.env['user.national.place'].create({
  #           'name': place['name'],
  #           'codename': place['codename']
  #         })
  #       except Exception as e:
  #         pass
