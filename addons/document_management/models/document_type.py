from odoo import models, fields

class DocumentType(models.Model):
    _name = 'document.type'
    _description = 'Document Type'
    
    name = fields.Char(string='Tên')
    short_name = fields.Char(string='Viết tắt')