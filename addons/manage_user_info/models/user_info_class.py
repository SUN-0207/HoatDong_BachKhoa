from odoo import models, fields, api


class UserInfoClass(models.Model):
 _name = 'user.info.class'
 _description = 'User Info Class'


 name = fields.Char('Class', required=True)
 major_id = fields.Many2one('user.info.major', string='Major', domain="[('name', '=', major_id)]")
#  department_id = fields.Many2one('user.info.department', string='Department')
 user_ids = fields.One2many('user.info', 'user_info_class_id', string='User')

_sql_constraints = [
    ('unique_class_name','UNIQUE (name)', 'Class name must be unique!')
    ]