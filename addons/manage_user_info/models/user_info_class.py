from odoo import models, fields, api


class UserInfoClass(models.Model):
    _name = 'user.info.class'
    _description = 'User Info Class'
    
    name = fields.Char('Class', required=True, translate=True)
    year = fields.Char('Year', compute="_compute_year_in", store=True)
    major_id = fields.Many2one('user.info.major', string='Major')

    _sql_constraints = [
        ('unique_class_name','UNIQUE (name)', 'Class name must be unique!')
        ]

    @api.depends('name')
    def _compute_year_in(self):
        for record in self:
            if record.name:
                year_prefix = record.name[2:4]
                record.year = str(int(year_prefix) + 2000)