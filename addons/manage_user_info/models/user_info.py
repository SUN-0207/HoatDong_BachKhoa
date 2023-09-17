from odoo import models, fields,api

class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  first_name = fields.Char('Firts Name',compute='_compute_name_parts', store=True)
  sur_name = fields.Char('Sur Name',compute='_compute_name_parts', store=True)
  
  user_id = fields.Many2one('res.users',string="User", required=True, ondelete='cascade', delegate=True, default=lambda self: self.env.uid)
  avatar = fields.Binary(related='user_id.image_128', string='Avatar', readonly=True)
  user_info_contact_id = fields.Many2one('user.info.contact', ondelete='cascade', delegate=True)
  # user_info_major_id = fields.Many2one('user.info.major',string='Major', required=True, ondelete='cascade')
  # user_info_department_id = fields.Many2one('user.info.department',string='Department', required=True, ondelete='cascade')
  # user_info_class_id = fields.Many2one('user.info.class',string='Class', required=True, ondelete='cascade')
 
  @api.depends('name')
  def _compute_name_parts(self):
    for user in self:
      if user.name:
        name_parts = user.name.split(" ")
        user.first_name = name_parts[0]
        user.sur_name = " ".join(name_parts[1:]) 
  
  
  
