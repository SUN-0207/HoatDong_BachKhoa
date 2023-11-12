from odoo import api, fields, models, _

class EventType(models.Model):
    _name = 'event.type'
    _inherit = 'event.type'

    name = fields.Char(string='Nhóm hoạt động')
    limited_registration = fields.Selection(
        [('limited', 'Giới hạn'), ('unlimited', 'Không giới hạn')],
        string='Giới hạn số hoạt động',
        required=True, default='unlimited'
    )
    max_event_registration = fields.Integer(string='Số hoạt động đăng ký tối đa', default=0, required=True)
    event_registed = fields.Integer(string='Số hoạt động đã đăng ký', default=0, readonly=True, store=True)
    is_available = fields.Boolean(store=True, default=True)
    max_social_working_day = fields.Integer(string='Số ngày CTXH tối đa', default=0, required=True)
    max_training_point = fields.Integer(string='ĐRL tối đa', required=True,  default=0)

    auto_accept_activity = fields.Boolean('Tự động đồng ý hoạt động', default=False)
  
    