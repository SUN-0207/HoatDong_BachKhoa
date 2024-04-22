from odoo import api, fields, models

class EventEvent(models.Model):
    """ Override Event model to add optional questions when buying tickets. """
    _inherit = 'event.event'

    question_ids = fields.One2many('event.question', 'event_id', 'Câu hỏi', copy=True, readonly=False, store=True)