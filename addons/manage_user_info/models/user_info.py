from odoo import models, fields,api

from . import common_constants
class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  user_id = fields.Many2one('res.users', string='User', readonly=True)
  
  name= fields.Char(related='user_id.name', string="Name")
  email= fields.Char(related='user_id.email', string="Email")
  avatar = fields.Binary(string='Avatar')
  first_name = fields.Char('First Name',compute='_compute_name_parts')
  sur_name = fields.Char('Sur Name',compute='_compute_name_parts')

  
  phone_number = fields.Char(string="Phone number")
  gender = fields.Selection([('male', 'Male'),('female', 'Female')])
  birth_date = fields.Date(string="Birth Day")
  nation = fields.Char(string="Nation")
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
  province_id_native = fields.Many2one('user.province.info', 'Province (Native)', widget='selection')
  district_id_native = fields.Many2one('user.district.info', 'District (Native)', domain="[('province_id', '=', province_id_native)]", widget='selection')
  ward_id_native = fields.Many2one('user.ward.info', 'Ward (Native)', domain="[('district_id', '=', district_id_native)]", widget='selection')
  
  permanent_address = fields.Char(string="Permanent Address")
  permanent_address_specific = fields.Char(string="Permanent Address Specific")
  province_id_permanent = fields.Many2one('user.province.info', 'Province (Permanent)', widget='selection')
  district_id_permanent = fields.Many2one('user.district.info', 'District (Permanent)', domain="[('province_id', '=', province_id_permanent)]", widget='selection')
  ward_id_permanent = fields.Many2one('user.ward.info', 'Ward (Permanent)', domain="[('district_id', '=', district_id_permanent)]", widget='selection')

  student_id = fields.Char(string="Student ID")
  user_info_department_id = fields.Many2one('user.info.department',string='Department', widget='selection')
  user_info_major_id = fields.Many2one('user.info.major',string='Major', widget='selection')
  user_info_class_id = fields.Many2one('user.info.class',string='Class')
  
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
   
  @api.depends('name')
  def _compute_name_parts(self):
    for user in self:
      if user.name:
        name_parts = user.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 
  
class ResUsers(models.Model):
  _inherit = ['res.users']
  
  user_info_id = fields.One2many('user.info', 'user_id', string='User Info', ondelete='set null')
  
  @api.model
  def create(self, vals):
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
  
  
  
  
  
  
