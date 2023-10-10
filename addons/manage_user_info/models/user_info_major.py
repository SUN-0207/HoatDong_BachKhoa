from odoo import models, fields, api


class UserInfoMajor(models.Model):
   _name = 'user.info.major'
   _description = 'User Info Major'

   name = fields.Char('Major', required=True)

   department_id = fields.Many2one('user.info.department', string='Department')
   class_ids = fields.One2many('user.info.class', 'major_id', string="Classes")

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