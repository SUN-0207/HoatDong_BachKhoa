from odoo import models, fields

class UserDepartmentAdmin(models.Model):
	_name = 'user.department.admin'
	_description = 'User Department Admin'

	name = fields.Char(string='Tên Quản lý Đơn bị', required=True)
	email = fields.Char(string='Email Quản lý Đơn bị', required=True)
	department_id = fields.Many2one('user.info.department', string='Đơn vị', required=True)

class UserSuperAdmin(models.Model):
  _name = 'user.super.admin'
  _description = 'User Super Admin'
  
  name = fields.Char(string='Tên Quản trị Hệ thống', required=True)
  email = fields.Char(string='Email Quản trị Hệ thống', required=True)
  
  