from odoo import models, fields


class UserInfoMajor(models.Model):
 _name = 'user.info.major'
 _description = 'User Info Major'

 name = fields.Char('Najor', required=True)

 department_id = fields.Many2one('user.info.department', string='Department')
 class_ids = fields.One2many('user.info.class', 'major_id', string='Class')
#  user_ids = fields.One2many('user.info', 'user_info_major_id', string='User')