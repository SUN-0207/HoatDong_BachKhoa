from odoo import models, fields,api

class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  first_name = fields.Char('Firts Name',compute='_compute_name_parts', store=True)
  sur_name = fields.Char('Sur Name',compute='_compute_name_parts', store=True)
  user_id = fields.Many2one('res.users',string="User", required=True, ondelete='cascade', delegate=True)
  # user_info_major_id = fields.Many2one('user.info.major',string='Major', required=True, ondelete='cascade')
  # user_info_department_id = fields.Many2one('user.info.department',string='Department', required=True, ondelete='cascade')
  # user_info_contact_id = fields.Many2one('user.info.contact',string='Personal Contact', required=True, ondelete='cascade')
  # user_info_class_id = fields.Many2one('user.info.class',string='Class', required=True, ondelete='cascade')
  
  @api.depends('name')
  def _compute_name_parts(self):
    for user in self:
      if user.name:
        name_parts = user.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 
        
  from odoo import models, fields, api
import requests

class UserInfoContact(models.Model):
    _name = 'user.info.contact'
    _description = 'User Info Contact'

    contact_id = fields.Many2one('user.info', string="User id", ondelete='cascade', delegate=True)

    province = fields.Selection(
        selection='_get_province_data',
        string='Province',
    )

    district = fields.Selection(
        string='District',
        selection='_get_districts',
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

    @api.depends('province')
    def _get_districts(self):
        if self.province:
            options = []
            response = requests.get("https://provinces.open-api.vn/api/d/")
            response.raise_for_status()
            data = response.json()
            for district_data in data:
                if district_data['province_code'] == self.province:
                    options.append((district_data['code'], district_data['name']))
            return options
        else:
            return []

    @api.onchange('province')
    def _onchange_province(self):
        if self.province:
            self.district = False


  
  
