from odoo import models, fields, api


class UserInfoClass(models.Model):
 _name = 'user.info.class'
 _description = 'User Info Class'


 name = fields.Char('Ten lop', required=True)
 major_id = fields.Many2one('user.info.major', string='Ten nganh')
 department_id = fields.Many2one('user.info.department', string='Ten don vi')

#  _sql_constraints = [
#    ('unique_class_name','unique(name)', 'class name must be unique')
#  ]