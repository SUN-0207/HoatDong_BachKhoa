from odoo import api, fields, models

class EventTagCategory(models.Model):
    _name = 'event.tag.category'
    _inherit = 'event.tag.category'

    # @api.model
    # def init(self):
    #     is_existed = self.env['event.tag.category'].search([('name', '=', 'Meaning')], limit=1)
    #     if not is_existed:
    #         self.env['event.tag.category'].create({
    #             'name': 'Meaning',
    #             'sequence': 1,
    #         })


class EventTag(models.Model):
    _name = 'event.tag'
    _inherit = 'event.tag'

    category_id = fields.Many2one(
        "event.tag.category",
        string="Category",
        required=True,
        ondelete='cascade',
        default=lambda self: self.env.ref('manage_activity.default_category', raise_if_not_found=False),
    )
