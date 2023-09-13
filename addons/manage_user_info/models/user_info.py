from odoo import models, fields

class UserInfo(models.Model):
  _name = 'user.info'
  _description = 'User Info'
  
  first_name = fields.Char('Firts name', required=True)
  surname = fields.Char('Surname', required=True)
  # field email available before
  user_id = fields.Many2one('res.users', required=True, ondelete='cascade', delegate=True)
  user_info_major_id = fields.Many2one('user.info.major',string='Major', required=True, ondelete='cascade')
  user_info_department_id = fields.Many2one('user.info.department',string='Department', required=True, ondelete='cascade')
  user_info_contact_id = fields.Many2one('user.info.contact',string='Personal Contact', required=True, ondelete='cascade')
  user_info_class_id = fields.Many2one('user.info.class',string='Class', required=True, ondelete='cascade')
  
  
