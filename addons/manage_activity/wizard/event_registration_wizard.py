from odoo import fields, models
from odoo.exceptions import ValidationError

class EventRegistrationWizard(models.TransientModel):
    _name = "event.registration.wizard"

    name = fields.Char(string="Họ và tên", default=lambda self: self.env.user.user_info_id.name)
    email = fields.Char(string="Email", default=lambda self: self.env.user.login)
    mssv = fields.Char(string="MSSV", default=lambda self: self.env.user.user_info_id.student_id)
    phone = fields.Char(string="Số điện thoại", default=lambda self: self.env.user.user_info_id.phone_number) 
    
    def register_event(self):
      self.ensure_one()
      event_id = self.env.context['active_id']
      current_event = self.env['event.event'].search([('id','=',event_id)],limit=1)
      current_event_ticket_ids = current_event.event_ticket_ids
      create_date = fields.Datetime.now()
      exist_resgistration = self.env['event.registration'].search([('event_id','=',event_id),('email','=',self.env.user.login)],limit=1)
      if exist_resgistration:
        raise ValidationError('Sự kiện đã được đăng ký')
      if self.env.user.has_group('manage_user_info.group_hcmut_user') and current_event_ticket_ids:
        flag = False
        for ticket_id in current_event_ticket_ids:
          print(ticket_id.event_department_id.name)
          print(ticket_id.event_info_major_id.name)
          print(ticket_id.event_info_academy_year.name)
          if ticket_id.event_department_id.id == self.env.user.user_info_id.user_info_department_id.id or ticket_id.event_department_id.name == "Tất cả":
            if ticket_id.event_info_major_id.id == self.env.user.user_info_id.user_info_major_id.id or ticket_id.event_info_major_id.name == "Tất cả":
              if ticket_id.event_info_academy_year.id == self.env.user.user_info_id.user_info_academy_year.id or ticket_id.event_info_academy_year.name == "Tất cả":
                if ticket_id.is_sold_out:
                  raise ValidationError("Nhóm đăng ký của bạn đã đủ số lượng đăng ký")
                flag = True
                registration = self.env['event.registration'].create({
                  'create_date': create_date,
                  'event_id': event_id,
                  'name': self.name,
                  'email': self.email,
                  'event_ticket_id': ticket_id.id,
                  'phone': self.phone
                })
                if current_event.auto_confirm:
                  registration.sudo().action_confirm()
                current_event.sudo().compute_event_registed_button()
                break
        if not flag:
          raise ValidationError("Bạn không được phép đăng ký hoạt động này")
      return self.notify_success()
    
    def notify_success(self):
      return {
          'type': 'ir.actions.client',
          'tag': 'display_notification',
          'params': {
              'title': 'Thành công',
              'message': 'Thao tác của bạn đã được lưu',
              'type': 'success',
              'sticky': False, 
              'next': {'type': 'ir.actions.act_window_close'},
          },
      }
      
