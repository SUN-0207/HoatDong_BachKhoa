from odoo import models, fields, api, _, Command
from odoo.exceptions import ValidationError
	
class UserSuperAdmin(models.Model):
  _name = 'user.super.admin'
  _description = 'User Super Admin'
  
  name = fields.Char(string='Tên Quản trị Hệ thống', required=True)
  email = fields.Char(string='Email Quản trị Hệ thống', required=True)
  
  @api.model
  def create(self, vals):
    group_super_admin_id = self.env['res.groups'].sudo().search([('name','=','Super Admin')], limit=1).id
    user = self.env['res.users'].search([('login','=',vals['email'])],limit=1)
    if user:
      user.write({
				'groups_id': [(6, 0, [group_super_admin_id])],
			})
    return super(UserSuperAdmin, self).create(vals)
  
  def write(self,vals):
    res = super(UserSuperAdmin, self).write(vals)
    print('update')
    return res
  
  def unlink(self):
    for admin in self:
      print(admin)
      user = self.env['res.users'].search([('login','=',admin.email)],limit=1)
      if user:
        user.unlink()
    return super(UserSuperAdmin,self).unlink()
  

class UserDpartmentAdmin(models.Model):
  _name = 'user.department.admin'
  _description = 'User Department Admin'
  
  name = fields.Char(string='Tên Quản lý Đơn vị', required=True)
  email = fields.Char(string='Email Quản lý Đơn vị', required=True)
  department_id = fields.Many2one('user.info.department', string='Đơn vị', required=True)
  
  @api.model
  def create(self, vals):
    group_department_admin_id = self.env['res.groups'].sudo().search([('name','=','Department Admin')], limit=1).id
    user = self.env['res.users'].search([('login','=',vals['email'])],limit=1)
    if user:
      user.write({
				'groups_id': [(6, 0, [group_department_admin_id])],
				'manage_department_id': vals['department_id'].id
			})
    return super(UserDpartmentAdmin, self).create(vals)
  
  def write(self,vals):
    res = super(UserDpartmentAdmin, self).write(vals)
    return res
  
  def unlink(self):
    for admin in self:
      user = self.env['res.users'].search([('login','=',admin.email)],limit=1)
      if user:
        user.unlink()
    return super(UserDpartmentAdmin,self).unlink()
  
  

  
  