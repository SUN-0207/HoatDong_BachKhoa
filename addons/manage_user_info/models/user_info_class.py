from odoo import models, fields, api


class UserInfoClass(models.Model):
 _name = 'user.info.class'
 _description = 'User Info Class'

 name = fields.Char('Class', required=True, translate=True)
 major_id = fields.Many2one('user.info.major', string='Major')

_sql_constraints = [
    ('unique_class_name','UNIQUE (name)', 'Class name must be unique!')
    ]