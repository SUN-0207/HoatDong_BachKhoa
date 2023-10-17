from odoo import models, fields

class EventEvent(models.Model):
  _inherit = 'event.event'
  
  date_begin_registration = fields.Datetime(string='Ngày bắt đầu đăng ký', required=True, tracking=True)
  date_end_registration = fields.Datetime(string='Ngày kết thúc đăng ký', required=True, tracking=True)
  maxSocialPoint = fields.Char(string="Số ngày CTXH tối đa")
  
  