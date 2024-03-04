from odoo import api, fields, models, _
from odoo.exceptions import UserError

class EventQuestion(models.Model):
    _name = 'event.question'
    _rec_name = 'title'
    _order = 'sequence,id'
    _description = 'Event Question'

    title = fields.Char(required=True, translate=True)
    question_type = fields.Selection([
        ('simple_choice', 'Selection'),
        ('text_box', 'Text Input')], default='simple_choice', string="Question Type", required=True)

    event_type_id = fields.Many2one('event.type', 'Event Type', ondelete='cascade')
    event_id = fields.Many2one('event.event', 'Event', ondelete='cascade')
    answer_ids = fields.One2many('event.question.answer', 'question_id', "Answers", copy=True)
    sequence = fields.Integer(default=10)
    is_mandatory_answer = fields.Boolean('Mandatory Answer')

    @api.ondelete(at_uninstall=False)
    def _unlink_except_answered_question(self):
        if self.env['event.registration.answer'].search_count([('question_id', 'in', self.ids)]):
            raise UserError(_('You cannot delete a question that has already been answered by attendees.'))

    # def action_view_question_answers(self):
    #     """ Allow analyzing the attendees answers to event questions in a convenient way:
    #     - A graph view showing counts of each suggestions for simple_choice questions
    #       (Along with secondary pivot and tree views)
    #     - A tree view showing textual answers values for text_box questions. """
    #     self.ensure_one()
    #     action = self.env["ir.actions.actions"]._for_xml_id("website_event_questions.action_event_registration_report")
    #     action['domain'] = [('question_id', '=', self.id)]
    #     if self.question_type == 'simple_choice':
    #         action['views'] = [(False, 'graph'), (False, 'pivot'), (False, 'tree')]
    #     elif self.question_type == 'text_box':
    #         action['views'] = [(False, 'tree')]
    #     return action

# ONLY ANSWERS THAT ADMIN SETUP ON MULTIPLE CHOICES QUESTION
class EventQuestionAnswer(models.Model):
    """ Contains suggested answers to a 'simple_choice' event.question. """
    _name = 'event.question.answer'
    _order = 'sequence,id'
    _description = 'Event Question Answer'

    name = fields.Char('Answer', required=True, translate=True)
    question_id = fields.Many2one('event.question', required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_selected_answer(self):
        if self.env['event.registration.answer'].search_count([('value_answer_id', 'in', self.ids)]):
            raise UserError(_('You cannot delete an answer that has already been selected by attendees.'))
