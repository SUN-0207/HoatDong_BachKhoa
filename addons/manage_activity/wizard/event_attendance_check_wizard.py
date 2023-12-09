from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class EventAttendanceCheckWizard(models.TransientModel):
    _name = "event.attendance.check.wizard"
    
    event_id = fields.Many2one('event.event', string='Event', readonly=True)
    mssv = fields.Char(string="MSSV", default_focus=True)
    name_student = fields.Char(string="Tìm tên sinh viên", readonly=True, compute='find_name')
    
         
    @api.depends('mssv')
    def find_name(self):
        self.ensure_one()
        if self.mssv:
            registration = self.env['event.registration'].search([('event_id','=', self.event_id.id),('user_info_mssv','=', self.mssv)],limit=1)
            if registration:
                self.name_student = registration.user_info_name
                self.attendance_check()
            else:
                self.name_student = "Sinh viên chưa đăng ký hoạt động này!"
        else:
            self.name_student = "Sinh viên chưa đăng ký hoạt động này!"

    def attendance_check(self):
        self.ensure_one()
        registration = self.env['event.registration'].search([('event_id','=', self.event_id.id),('user_info_mssv','=', self.mssv)],limit=1)
        if registration:
            registration.write({'time_check_attendace': registration.time_check_attendace + 1})
            self.env['event.attendance.check'].create({
                'event_id': self.event_id.id,
                'registration_id': registration.id,
                'time_check': registration.time_check_attendace
            })
            self.mssv = ""
        else:
            self.name_student = "Sinh viên chưa đăng ký hoạt động này!"

    def close_wizard(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {
                'action': {
                    'type': 'ir.actions.act_window_close',
                },
            },
        }
        
    def notify_success(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Điểm danh thành công',
                'type': 'success',
                'sticky': False,
            },
        }
    
    def notify_fail(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thất bại',
                'message': 'Điểm danh không thành công',
                'type': 'danger',
                'sticky': False,
            },
        }