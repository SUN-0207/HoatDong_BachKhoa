from odoo import models, fields

class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'
    
    name = fields.Char(string='Ten')
    short_name = fields.Char(string='Viet tat')
    