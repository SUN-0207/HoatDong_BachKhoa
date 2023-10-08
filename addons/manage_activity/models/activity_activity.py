from odoo import models, fields

class ActivityActivity(models.Model):
  _name = 'activity.activity'
  _description = 'Activity'
  
  name = fields.Char(string="Name", required=True)