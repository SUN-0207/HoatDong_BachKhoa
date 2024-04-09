from odoo import models, fields

class DocumentNumberBook(models.Model):
    _name = 'document.number.book'
    _description = 'Document Number Book'
    
    type_id = fields.Many2one('document.type', string='The loai')
    number_format_type = fields.Selection(
        string='The thuc',
        selection=[('DTN', 'Van ban Doan'), ('HSV', 'Van ban Hoi')]
    )
    current_number_document = fields.Integer(string='So luong van ban hien tai', default=0)
    current_symbol_number = fields.Char(string='So ki hieu hien tai')
    
    user_id = fields.Many2one('res.users', string='User', readonly=True)