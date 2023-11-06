from odoo import models, fields, api, exceptions

class EventRegistration(models.Model):
      _name = 'event.registration'
      _inherit = ['event.registration']
      _description = 'event Registration'

      status = fields.Char(string='Trang thai', readonly=True)
      event_id = fields.Many2one('event.event', string='event', readonly=True, store=True)

      event_name = fields.Char('Ten event', related='event_id.name', store=True)

      user_info_id = fields.Many2one('user.info', readonly=True, string='User Info', store=True)
      user_info_name = fields.Char('Ten user', related='user_info_id.name') 
      user_info_email= fields.Char('Email user', related='user_info_id.email') 
      user_info_phone_number= fields.Char('Phone ', related='user_info_id.phone_number') 
      user_info_gender= fields.Selection('Gender', related='user_info_id.gender') 
      user_info_student_id= fields.Char('MSSV', related='user_info_id.student_id') 
      user_info_department_id= fields.Many2one('user.info.department', 'Don vi', related='user_info_id.user_info_department_id') 
      user_info_major_id= fields.Many2one('user.info.major', 'Chuyen nganh', related='user_info_id.user_info_major_id') 
      user_info_class_id= fields.Many2one('user.info.class', 'Lop', related='user_info_id.user_info_class_id') 
      
      state = fields.Selection([
        ('draft', 'Unconfirmed'), ('cancel', 'Cancelled'),
        ('open', 'Confirmed'), ('done', 'Attended')],
        string='Status', default='draft', copy=False, tracking=True)
           
      @api.model
      def create(self, vals):
            #Check dieu kien o day
            print('Create Regis: ', vals)
            event_registration = super(EventRegistration, self).create(vals)
            return event_registration

      def write(self, vals):
            print('Update Regis: ', vals)
            result = super(EventRegistration, self).write(vals)
            # Add any additional logic you need upon updating a registration
            return result

      def confirm_action(self):
        self.ensure_one()
        if self.status:
            raise exceptions.ValidationError('This registration has already been confirmed.')

        self.status = 'Confirmed'
        return {'type': 'ir.actions.act_window_close'}

      def close_confirm(self):
            return {'type': 'ir.actions.act_window_close'}

      def _get_website_registration_allowed_fields(self):
            return {
                  'event_id', 
                  'partner_id', 
                  'event_ticket_id',
                  'name', 
                  'phone', 
                  'email', 
                  'phone_number',
                  }
