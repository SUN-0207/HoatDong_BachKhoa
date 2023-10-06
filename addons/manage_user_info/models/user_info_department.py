from odoo import models, fields, api


class UserInfoDepartment(models.Model):
    _name = 'user.info.department'
    _description = 'User Info Department'
 
    name = fields.Char('Department', required=True, translate=True)
    code = fields.Char('Department code', required=True)
 
    major_ids = fields.One2many('user.info.major', 'department_id', string='Major')
    user_manage_ids = fields.One2many('res.users', 'manage_department_id')
    major_count = fields.Integer('Major count', compute="_compute_major_count", store=True, default=0)

    @api.depends('major_ids')
    def _compute_major_count(self):
        for rec in self:
            rec.major_count = len(rec.major_ids)


    _sql_constraints = [
        ('unique_department_name','UNIQUE (name)', 'Department name must be unique'),
        ('unique_department_code','UNIQUE (code)', 'Department code must be unique')
        ]