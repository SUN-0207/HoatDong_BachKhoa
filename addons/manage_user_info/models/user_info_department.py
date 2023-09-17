from odoo import models, fields


class UserInfoDepartment(models.Model):
 _name = 'user.info.department'
 _description = 'User Info Department'
 
 name = fields.Char('Department', required=True)
 code = fields.Char('Department code', required=True)
 
 major_ids = fields.One2many('user.info.major', 'department_id', string='Major')
#  class_ids = fields.One2many('user.info.class', 'department_id', string='Ten lop')
#  user = fields.One2many('user.info','user_info_department_id',string='User')

#   _sql_constraints = [
#    ('unique_department_name','unique(name)', 'department name must be unique')
#    ]