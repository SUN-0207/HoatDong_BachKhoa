from odoo import models, fields


class UserInfoMajor(models.Model):
 _name = 'user.info.major'
 _description = 'User Info Major'

 name = fields.Char('Ten nganh', required=True)
 class_ids = fields.One2many('user.info.class', 'name', string='Ten lop')
 department_id = fields.Many2one('user.info.department', string='Ten don vi')