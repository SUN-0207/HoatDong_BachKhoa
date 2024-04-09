from odoo import models, fields, api
from odoo.exceptions import AccessDenied, ValidationError, UserError


class Document(models.Model):
    _name = "document"
    _description = "Document"

    name = fields.Char(string="Trich yeu")
    type_id = fields.Many2one("document.type", string="The loai")
    symbol_number_format_type = fields.Selection(
        string="The thuc", selection=[("DTN", "Van ban Doan"), ("HSV", "Van ban Hoi")]
    )
    symbol_number = fields.Char(string="So ki hieu")
    previous_symbol_number = fields.Char(string="So ki hieu truoc do")
    user_sign = fields.Char(string="Nguoi ky")

    is_public = fields.Boolean(default=False)
    public_date = fields.Date(string="Ngay ban hanh")

    attach_file = fields.Binary(string="File dinh kem")

    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user
    )

    @api.model
    def create(self, vals):
        document_book = self.env["document.number.book"].search(
            [
                ("type_id.id", "=", vals['type_id']),
                ("number_format_type", "=", vals['symbol_number_format_type']),
            ],
            limit=1,
        )
        next_number = document_book.current_number_document + 1
        vals.update({
            'previous_symbol_number': document_book.current_symbol_number
        })
        document_book.sudo().write(
            {
                'current_number_document': next_number,
                'current_symbol_number': vals['symbol_number']
            }
        )
        
        return super(Document, self).create(vals)

    def write(self, vals):
        print(self, vals, "write")
        return super(Document, self).write(vals)
    
    def unlink(self):
        for document in self:
            if document.is_public:
                raise ValidationError(_('Khong the xoa van ban da ban hanh'))
            
            document_book = self.env["document.number.book"].search(
                [
                    ("type_id.id", "=", document.type_id.id),
                    ("number_format_type", "=", document.symbol_number_format_type),
                ],
                limit=1,
            )
            
            update_number_document = document_book.current_number_document - 1
            
            document_book.sudo().write({
                'current_number_document': update_number_document,
                'current_symbol_number': document.previous_symbol_number
            })
        return super(Document, self).unlink()
    
    @api.onchange("type_id", "symbol_number_format_type")
    def _compute_symbol_number(self):
        for document in self:
            if document.type_id and document.symbol_number_format_type:
                document_number_book = self.env["document.number.book"].search(
                    [
                        ("type_id.id", "=", document.type_id.id),
                        ("number_format_type", "=", document.symbol_number_format_type),
                    ],
                    limit=1,
                )
                next_number = document_number_book.current_number_document + 1
                if document.symbol_number_format_type == "DTN":
                    document.symbol_number = (
                        f"0{next_number}-{document.type_id.short_name}/DTN"
                        if next_number < 10
                        else f"{next_number}-{document.type_id.short_name}/DTN"
                    )
                if document.symbol_number_format_type == "HSV":
                    document.symbol_number = (
                        f"0{next_number}/{document.type_id.short_name}-HSV"
                        if next_number < 10
                        else f"{next_number}/{document.type_id.short_name}-HSV"
                    )
            else:
                document.symbol_number = ""
    
    def initial_document_book(self):
        document_type_list = self.env['document.type'].search([])
        for document_type in document_type_list:
            document_book = self.env['document.number.book'].search([('type_id.id', '=', document_type.id),('user_id.id', '=', self.env.uid)])
            if not document_book:
                self.env['document.number.book'].sudo().create([
                    {
                        'type_id': document_type.id,
                        'user_id': self.env.uid,
                        'number_format_type': 'DTN',
                        'current_number_document': 0,
                    },
                    {
                        'type_id': document_type.id,
                        'user_id': self.env.uid,
                        'number_format_type': 'HSV',
                        'current_number_document': 0,
                    }
                ])
                
    def open_document_list(self):
        self.initial_document_book()
        action = {
            'name': 'Document',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'document',
            'domain': [('user_id.id', '=', self.env.uid)],
            'limit': 15,
        }
        return action   

