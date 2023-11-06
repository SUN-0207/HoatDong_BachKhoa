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
      create_date = fields.Datetime.now()
      exist_resgistration = self.env['event.registration'].search([('event_id','=',event_id),('email','=',self.env.user.login)],limit=1)
      if exist_resgistration:
        raise ValidationError('Sự kiện đã được đăng ký')
      registration = self.env['event.registration'].create({
        'create_date': create_date,
        'event_id': event_id,
        'name': self.name,
        'email': self.email,
        'phone': self.phone
      })
      if current_event.auto_confirm:
        registration.sudo().action_confirm()
      current_event.sudo().compute_event_registed_button()
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
      
