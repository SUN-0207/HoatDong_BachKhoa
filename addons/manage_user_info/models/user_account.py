from odoo import models, fields

class UserDepartmentAdmin(models.Model):
	_name = 'user.department.admin'
	_description = 'User Department Admin'

	name = fields.Char(string='Department Admin Name')
	email = fields.Char(string='Deparment Admin Email')
	department_id = fields.Many2one('user.info.department', string='Department')

class UserSuperAdmin(models.Model):
  _name = 'user.super.admin'
  _description = 'User Super Admin'
  
  name = fields.Char(string='Super Admin Name')
  email = fields.Char(string='Super Admin Email')
  
  