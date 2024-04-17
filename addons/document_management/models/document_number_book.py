from odoo import models, fields, api

class DocumentNumberBook(models.Model):
    _name = 'document.number.book'
    _description = 'Document Number Book'
    
    type_id = fields.Many2one('document.type', string='Thể loại')
    number_format_type = fields.Selection(
        string='Thể thức',
        selection=[('DTN', 'Văn bản Đoàn'), ('HSV', 'Văn bản Hội')]
    )
    current_number_document = fields.Integer(string='Số lượng văn bản hiện tại', default=0)
    current_symbol_number = fields.Char(string='Số kí hiệu hiện tại')
    
    user_id = fields.Many2one('res.users', string='User', readonly=True)
    