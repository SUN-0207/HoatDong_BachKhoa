from odoo import models, fields, api


class UserInfoClass(models.Model):
    _name = 'user.info.class'
    _description = 'User Info Class'
    
    name = fields.Char('Class', required=True)
    
    student_ids = fields.One2many('user.info', 'user_info_class_id', string='Students')
    student_count = fields.Integer('Student Count', compute="_compute_student_count", store=True, default=0)
    
    major_id = fields.Many2one('user.info.major', string='Major')
    year_id = fields.Many2one('user.info.year', string='Year', compute="_compute_year_in", store=True)
    is_year_active = fields.Boolean(string="Check year active", readonly=True, compute="_check_year_active")

    @api.depends('year_id')
    def _check_year_active(self):
        for record in self:
            record.is_year_active = record.year_id.is_enable
    
    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    _sql_constraints = [
        ('unique_class_name','UNIQUE (name)', 'Class name must be unique!')
        ]
    
    def open_list_class_info(self):
        action = {
            'name': 'Thông tin Lớp học',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'user.info.class',  
        }
        if self.env.user.manage_department_id:
            action.update({
                'domain': [('major_id','in',self.env.user.manage_department_id.major_ids.ids)]
            })
        return action 

    @api.onchange('name')
    def _compute_year_in(self):
        for record in self:
            if record.name:
                year_prefix = record.name[2:4]
                year_name = str(int(year_prefix) + 2000)
                year = self.env['user.info.year'].search([('name', '=', year_name)], limit=1)
                record.year_id = year.id if year else False