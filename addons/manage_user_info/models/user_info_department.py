from odoo import models, fields, api


class UserInfoDepartment(models.Model):
    _name = 'user.info.department'
    _description = 'User Info Department'
 
    name = fields.Char('Đơn vị', required=True, translate=True)
    code = fields.Char('Mã đơn vị', required=True)
 
    major_ids = fields.One2many('user.info.major', 'department_id', string='Ngành')
    user_manage_ids = fields.One2many('res.users', 'manage_department_id')
    major_count = fields.Integer('Số ngành', compute="_compute_major_count", store=True, default=0)

    @api.depends('major_ids')
    def _compute_major_count(self):
        for rec in self:
            rec.major_count = len(rec.major_ids)


    _sql_constraints = [
        ('unique_department_name','UNIQUE (name)', 'Department name must be unique'),
        ('unique_department_code','UNIQUE (code)', 'Department code must be unique')
        ]