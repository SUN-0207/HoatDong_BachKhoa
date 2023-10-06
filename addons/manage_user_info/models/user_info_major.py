from odoo import models, fields, api


class UserInfoMajor(models.Model):
   _name = 'user.info.major'
   _description = 'User Info Major'

   name = fields.Char('Major', required=True)

   department_id = fields.Many2one('user.info.department', string='Department', readonly=True)
   year_ids = fields.One2many('user.info.year', 'major_id', string='Year')
   class_ids = fields.One2many('user.info.class', 'major_id', string="Classes")
   # is_year_active = fields.Boolean(string="Check year active", readonly=True, compute="_check_year_active")

   # @api.depend('year_ids')
   # def _check_year_active(self):
   #    for record in self:
   #       record.is_year_active = record.year_ids.is_enable


   def open_list_major_info(self):
      action = {
         'name': 'Thông tin Ngành học',
         'type': 'ir.actions.act_window',
         'view_mode': 'tree,form',
         'res_model': 'user.info.major',  
      }
      if self.env.user.manage_department_id:
         action.update({
            'domain': [('department_id','=',self.env.user.manage_department_id.id)]
         })
      return action  

   _sql_constraints = [
      ('unique_major_name','UNIQUE (name)', 'Major name must be unique')
      ]