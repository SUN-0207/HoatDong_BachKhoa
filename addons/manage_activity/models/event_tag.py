from odoo import api, fields, models

class EventTag(models.Model):
    _name = 'event.tag'
    _inherit = 'event.tag'


class EventTagCategory(models.Model):
    _name = 'event.tag.category'
    _inherit = 'event.tag.category'

    @api.model
    def init(self):
        is_existed = self.env['event.tag.category'].search([('name', '=', 'Meaning')], limit=1)
        if not is_existed:
            self.env['event.tag.category'].create({
                'name': 'Meaning',
            })
