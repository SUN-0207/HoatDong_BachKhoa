from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class EventAttendanceCheckWizard(models.TransientModel):
    _name = "event.attendance.check.wizard"
    
    event_id = fields.Many2one('event.event', string='Event', readonly=True)
    mssv = fields.Char(string="MSSV", default_focus=True)
    name_student = fields.Char(string="Tìm tên sinh viên", readonly=True, compute='find_name')
    
         
    @api.depends('mssv')
    def find_name(self):
        for record in self:
            if record.mssv:
                record.name_student = ""
                res = (self.env['event.registration'].search([('event_id','=', self.event_id.id)]))
                for regis in res:
                    if regis.user_info_mssv == record.mssv:
                        record.name_student = regis.user_info_name
            else:
                record.name_student = "Sinh viên chưa đăng ký hoạt động này!"



    def attendance_check(self):
        self.ensure_one()
        res = (self.env['event.registration'].search([('event_id','=', self.event_id.id)]))
        print(self.mssv)
        for regis in res:
            if(regis.user_info_mssv == self.mssv):
                regis.write({'time_check_attendace': regis.time_check_attendace + 1})
                self.env['event.attendance.check'].create({
                    'event_id': self.event_id.id,
                    'registration_id': regis.id,
                    'time_check': regis.time_check_attendace
                })
                self.mssv = ""
                return self.notify_success()
        return self.notify_fail()      

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