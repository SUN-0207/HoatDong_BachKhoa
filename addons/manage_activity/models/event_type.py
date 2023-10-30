from odoo import api, fields, models, _

class EventType(models.Model):
    _name = 'event.type'
    _inherit = 'event.type'

    name = fields.Char(string='Nhóm hoạt động')
    limited_registration = fields.Selection(
    [('limited', 'Giới hạn'), ('unlimited', 'Không giới hạn')],
    string='Giới hạn số hoạt động',
    required=True, default='limited'
    )
    max_event_registration = fields.Integer(string='Số hoạt động đăng ký tối đa')
    max_social_working_day = fields.Integer(string='Số ngày CTXH tối đa', required=True)
    max_training_point = fields.Integer(string='Số ĐRL tối đa', required=True)

    auto_accept_activity = fields.Boolean('Tu dong duyet', default=False)
  
 