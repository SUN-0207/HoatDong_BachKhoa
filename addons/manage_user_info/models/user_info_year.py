from odoo import models, fields

class UserInfoYear(models.Model):
    _name = 'user.info.year'
    _description = 'User Info Academy Year'
    
    name = fields.Char(string='Year', required=True, store=True)

    is_enable = fields.Boolean(string='Is enable', required=True, store=True, default=True)

    student_ids = fields.One2many('user.info', 'user_id')
    
    major_id = fields.Many2one('user.info.major', string="Major")
    class_ids = fields.One2many('user.info.class', 'year_id', string='Class')