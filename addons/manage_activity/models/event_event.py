from odoo import models, fields, api,SUPERUSER_ID
from odoo.exceptions import ValidationError
class EventEvent(models.Model):
  _inherit = 'event.event'
  
  user_id = fields.Many2one('res.users', string='User', readonly=True)
  activity_manager =  fields.Many2many('user.department.admin', string='Giam sat')
  created_by_name = fields.Char(string="Hoat dong duoc tao boi ", store=True, default = lambda self: self.env.user.name)

  #Xoa default khong duoc => chac xoa tay
  @api.model
  def uninstall_hook(self):
        unwanted_stages = ['event_stage_new', 'event_stage_booked', 'event_stage_announced', 'event_stage_done', 'event_stage_cancelled']
        stages = self.env['event.stage'].search([('id', 'in', unwanted_stages)])
        stages.unlink()
  
  # status_activity = fields.Selection(
  #   string="Trạng thái",
  #   selection=[
  #       ('new', 'Mới'),
  #       ('need_update', 'Bổ sung'),
  #       ('accept', 'Đã duyệt'),
  #       ('cancel', 'Đã huỷ'),
  #       ('registration', 'Mở đăng ký'),
  #       ('inprogress', 'Đang diễn ra'),
  #       ('completed', 'Đã kết thúc')
  #   ],
  #   readonly=True,
  #   copy=False,
  #   default='new',
  # )

  #Kanban (cai tron tron goc phai tren)
  # kanban_state = fields.Selection([('normal', 'In Progress'), ('done', 'Done'), ('blocked', 'Blocked')], default='normal', copy=False)
  # kanban_state_label = fields.Char(
  #       string='Kanban State Label', compute='_compute_kanban_state_label',
  #       store=True, tracking=True)

  date_begin_registration = fields.Datetime(string='Ngày bắt đầu đăng ký', required=True, tracking=True)
  date_end_registration = fields.Datetime(string='Ngày kết thúc đăng ký', required=True, tracking=True)
  max_social_point = fields.Char(string="Số ngày CTXH tối đa")
  max_tranning_point = fields.Integer(string="DRL toi da")

  description = fields.Text(string="Nội dung hoạt động", widget="html" )
  attach_file = fields.Many2many('ir.attachment', string='Attachments', widget='many2many_binary')

  department_can_register = fields.Many2many('user.info.department', string='Department', default='False')
  major_can_register = fields.Many2many('user.info.major', string='Major')
  year_can_register = fields.Many2many('user.info.year', string='Years')

  @api.constrains('date_begin_registration', 'date_end_registration', 'date_begin', 'date_end')
  def _check_dates(self):
        for activity in self:
            if activity.date_begin_registration >= activity.date_end_registration:
                raise ValidationError('Ngay ket thuc dang ky phai sau ngay dang ky')
            if activity.date_begin >= activity.date_end:
                raise ValidationError('Ngay ket thuc phai sau ngay bat dau')
            if activity.date_begin_registration >= activity.date_end:
                raise ValidationError('Ngay bat dau dang ky phai truoc ngay ket thuc')


class ResUsers(models.Model):
  _inherit = ['res.users']

class UserDepartmentAdmin(models.Model):
  _inherit = ['user.department.admin']
class ActivityDepartment(models.Model):
  name = 'activity.department'
  _inherit = 'user.info.department'

  max_num_resgis = fields.Integer('So luong dang ky toi da')

class UserInfoMajor(models.Model):
  _inherit = 'user.info.major'
class UserInfoYear(models.Model):
  _inherit = 'user.info.year'