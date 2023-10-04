from odoo import models, fields

class UserInfoYear(models.Model):
    _name = 'user.info.year'
    _description = 'User Info Academy Year'
    
    name = fields.Char(string='Year', required=True, store=True)
    
    student_ids = fields.One2many('user.info', 'user_id')
    class_ids = fields.One2many('user.info.class', 'year_id', string='Class')
    major_id = fields.Many2one('user.info.major')