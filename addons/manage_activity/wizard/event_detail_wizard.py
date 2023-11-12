from odoo import models, fields, api

class EventDetailWizard(models.TransientModel):
    _name = 'event.detail.wizard'
    _description = 'Event Event Wizard'

    name = fields.Char(string='Tên hoạt động', required=True)
    stage_name = fields.Char(string='Tên tình trạng duyệt')
    status_activity = fields.Selection(
        string="Tình trạng hoạt động",
        selection=[
            ('new', 'Mới'),
            ('open_registration', 'Mở đăng ký'),
            ('close_registration', 'Đóng đăng ký'),
            ('inprogress', 'Đang diễn ra'),
            ('completed', 'Đã kết thúc')],
        copy=False,
        default=False,
        store=True,
    )

    active = fields.Boolean(string="Active")
    event_type_id = fields.Many2one('event.type')
    tag_ids = fields.Many2many('event.tag', string="Tags")

    date_begin_registration = fields.Datetime(string='Ngày bắt đầu đăng ký', required=True)
    date_end_registration = fields.Datetime(string='Ngày kết thúc đăng ký', required=True)
    date_begin = fields.Datetime(string='Start Date', required=True, tracking=True)
    date_end = fields.Datetime(string='End Date', required=True, tracking=True)
    
    max_social_point = fields.Char(string="Số ngày CTXH tối đa")
    max_tranning_point = fields.Integer(string="ĐRL tối đa")

    description = fields.Text(string="Mô tả hoạt động", widget="html")
    attach_file = fields.Many2many('ir.attachment', string='Attachments', widget='many2many_binary')

    is_for_all_students = fields.Boolean(string="Dành cho toàn bộ sinh viên", default=True)
