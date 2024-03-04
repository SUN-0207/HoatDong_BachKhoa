from odoo import fields, models
from odoo.exceptions import UserError, ValidationError

class EventRegistrationWizard(models.TransientModel):
    _inherit = "event.registration.wizard"

    question_answer_ids = fields.One2many('event.registration.wizard.answer', 'wizard_id', string="Question Answers")

    # Load questions of the event into wizard
    def default_get(self, fields):
        # print("get_event_questions() called")
        res = super(EventRegistrationWizard, self).default_get(fields)
        event_id = self.env.context['active_id']
        if event_id:
            event = self.env['event.event'].search([('id','=',event_id)],limit=1)
            questions = event.question_ids
            question_answers = []
            for question in questions:
                question_answers.append((0, 0, {
                    'wizard_id': self.id,
                    'question_id': question.id,  # Link the answer to the question
                    'question_title': question.title,
                    'question_type': question.question_type,
                    'multiple_choices': question.answer_ids
                }))
            
            res['question_answer_ids'] = question_answers
        return res

    def register_event(self):
      self.ensure_one()
      event_id = self.env.context['active_id']
      current_event = self.env['event.event'].search([('id','=',event_id)],limit=1)
      current_event_ticket_ids = current_event.event_ticket_ids
      create_date = fields.Datetime.now()
      
      exist_resgistration = self.env['event.registration'].search([('event_id','=',event_id),('email','=',self.env.user.login)],limit=1)
      if exist_resgistration:
        raise ValidationError('Sự kiện đã được đăng ký')
      
      if current_event.event_type_id.limited_registration == 'limited':
        check = current_event.event_type_id.max_event_registration
        user_event_registration= self.env['event.registration'].search([('email','=',self.env.user.login)])
        for event_registration in user_event_registration:
          event = event_registration.event_id
          if event.event_type_id.id == current_event.event_type_id.id:
            check -= 1
        if check <= 0:
          raise ValidationError("Số hoạt động bạn đăng ký trong nhóm này đã đạt tối đa")
                
      if self.env.user.has_group('manage_user_info.group_hcmut_user') and current_event_ticket_ids:
        flag = False
        for ticket_id in current_event_ticket_ids:
          if ticket_id.event_department_id.id == self.env.user.user_info_id.user_info_department_id.id or ticket_id.event_department_id.name == "Tất cả":
            if ticket_id.event_info_major_id.id == self.env.user.user_info_id.user_info_major_id.id or ticket_id.event_info_major_id.name == "Tất cả":
              if ticket_id.event_info_academy_year.id == self.env.user.user_info_id.user_info_academy_year.id or ticket_id.event_info_academy_year.name == "Tất cả":
                if ticket_id.is_sold_out:
                  raise ValidationError("Đối tượng sinh viên bạn thuộc đã đủ số lượng đăng ký")
                flag = True

                registration = self.env['event.registration'].create({
                  'create_date': create_date,
                  'event_id': event_id,
                  'name': self.name,
                  'email': self.email,
                  'event_ticket_id': ticket_id.id,
                  'phone': self.phone,
                  'user_info_id': self.env.user.user_info_id.id
                #   'registration_answer_ids': '',
                })

                registration_id = self.env['event.registration'].search([('event_id','=',event_id), ('user_info_id','=',self.env.user.user_info_id.id)], limit=1)
                # create answer:
                for answer in self.question_answer_ids: 
                    registration_answer = self.env['event.registration.answer'].create({
                        'question_id': answer.question_id.id,
                        'event_id': event_id,
                        'question_type': answer.question_type,
                        'value_answer_id': answer.value_answer_id,
                        'value_text_box': answer.value_text_box,
                        'registration_id': registration_id.id
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

class EventRegistrationWizardAnswer(models.TransientModel):
    _name = 'event.registration.wizard.answer'
    _description = 'Event Registration Wizard Answer'

    wizard_id = fields.Many2one('event.registration.wizard', string="Wizard")
    
    question_id = fields.Many2one('event.question', string="Question")  # to link to the question
    question_title = fields.Char(related="question_id.title", readonly=True)
    question_type = fields.Selection(related="question_id.question_type", readonly=True)
    multiple_choices = fields.One2many('event.question.answer', related="question_id.answer_ids")

    multiple_choices_selection =fields.Selection(string="selection!!", selection="_get_suggested_answers")

    def _get_suggested_answers(self):
        question = self.question_id
        return [(answer.name, answer.name) for answer in question.answer_ids]

    def _turn_one2many_into_selection(self):
        # print("_turn_one2many_into_selection(): ", self.multiple_choices)
        # question = self.env['event.question'].search([('id','=',self.question_id.id)],limit=1)
        options = []
        for choice in self.multiple_choices:
            options.append((choice.id, choice.name))
        return options

    # multiple_choices_selection = fields.Selection(_turn_one2many_into_selection, string="Selction !!")

    value_answer_id = fields.Many2one('event.question.answer', string="Suggested answer")
    value_text_box = fields.Text(string="Text answer")

    def action_save(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window_close'
        }

    


