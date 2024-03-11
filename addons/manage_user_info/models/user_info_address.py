import requests
from odoo import models, fields, api
from vietnam_provinces.enums import ProvinceEnum, DistrictEnum
from vietnam_provinces.enums.wards import WardEnum

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
    
    # Get all provinces
    provinces_data = ProvinceEnum.__members__.values()
    
    for province_data in provinces_data:
      existing_province = self.env['user.province.info'].search([('code', '=', province_data.value.code)], limit=1)
      
      if not existing_province:
        # Create Province
        province = self.env['user.province.info'].create({
            'name': province_data.value.name,
            'code': province_data.value.code,
            'division_type': province_data.value.division_type.value,
            'codename': province_data.value.codename,
            'phone_code': province_data.value.phone_code,
        })
        
        # Get districts of the province
        districts_data = DistrictEnum.__members__.values()
        
        for district_data in districts_data:
          if district_data.value.province_code == province_data.value.code:
              district = self.env['user.district.info'].create({
                  'name': district_data.value.name,
                  'code': district_data.value.code,
                  'division_type': district_data.value.division_type.value,
                  'codename': district_data.value.codename,
                  'province_id': province.id,
              })
              
              # Get wards of the district
              wards_data = [ward for ward in WardEnum if ward.value.district_code == district_data.value.code]

              for ward_data in wards_data:
                  if ward_data.value.district_code == district_data.value.code:
                      self.env['user.ward.info'].create({
                          'name': ward_data.value.name,
                          'code': ward_data.value.code,
                          'division_type': ward_data.value.division_type.value,
                          'codename': ward_data.value.codename,
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
    # Get all provinces
    provinces_data = ProvinceEnum.__members__.values()
    
    for province_data in provinces_data:
        existing_province = self.env['user.national.place'].search([('codename', '=', province_data.value.codename)], limit=1)

        if not existing_province:
            province = self.env['user.national.place'].create({
                'name': province_data.value.name,
                'codename': province_data.value.code,
            })