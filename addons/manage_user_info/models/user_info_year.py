from odoo import models, fields

class UserInfoYear(models.Model):
    _name = 'user.info.year'
    _description = 'User Info Academy Year'
    
    name = fields.Char(string='Niên khoá', required=True, store=True)

    is_enable = fields.Boolean(string='Hiển thị Niên khoá', required=True, default=True)
    show_student_form = fields.Boolean(default=True)
    
    student_ids = fields.One2many('user.info', 'user_id')
    
    class_ids = fields.One2many('user.info.class', 'year_id', string='Lớp')