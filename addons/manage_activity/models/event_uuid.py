from odoo import fields, models, _

class GeneratedUUID(models.Model):
    _name = 'generated.uuid'
    
    uuid = fields.Char(string='UUID', size=8)