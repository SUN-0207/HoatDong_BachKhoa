from odoo import models, fields


class UserInfoDepartment(models.Model):
 _name = 'user.info.department'
 _description = 'User Info Department'
 
 name = fields.Char('Department', required=True)
 code = fields.Char('Department code', required=True)
 
 major_ids = fields.One2many('user.info.major', 'department_id', string='Major')

_sql_constraints = [
    ('unique_department_name','UNIQUE (name)', 'Department name must be unique'),
    ('unique_department_code','UNIQUE (code)', 'Department code must be unique')
    ]