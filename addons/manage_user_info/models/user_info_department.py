from odoo import models, fields


class UserInfoDepartment(models.Model):
 _name = 'user.info.department'
 _description = 'User Info Department'
 
 name = fields.Char('Ten don vi', required=True)
 code = fields.Char('Ma don vi', required=True)
 major_ids = fields.One2many('user.info.class', 'department_id', string='Ma nganh')

#   _sql_constraints = [
#    ('unique_department_name','unique(name)', 'department name must be unique')
#    ]