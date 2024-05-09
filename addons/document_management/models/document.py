from odoo import models, fields, api
from odoo.exceptions import AccessDenied, ValidationError, UserError

class Document(models.Model):
    _name = "document"
    _description = "Document"

    name = fields.Char(string="Trích yếu")
    type_id = fields.Many2one("document.type", string="Thể loại")
    symbol_number_format_type = fields.Selection(
        string="Thể thức", selection=[("DTN", "Văn bản Đoàn"), ("HSV", "Văn bản Hội")]
    )
    symbol_number = fields.Char(string="Số kí hiệu")
    previous_symbol_number = fields.Char(string="Số kí hiệu trước")
    user_sign = fields.Char(string="Người ký")

    is_public = fields.Boolean(default=False)
    public_date = fields.Date(string="Ngày ban hành")

    attach_file = fields.Many2many('ir.attachment',string="File đính kèm")

    department_ids = fields.Many2many('user.info.department',string='Đơn vị nhận')
    
    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user
    )
    
    can_action_on_document = fields.Boolean(default=False)
    
    is_read_document = fields.Boolean(default=False)
    state_read_document = fields.Selection([('new', 'Mới'), ('done', 'Đã đọc')], string='Trạng thái')
    document_read_ids = fields.One2many('document.read', 'document_id', string='Đơn vị đã đọc')
    
    @api.model
    def create(self, vals):
        document_book = self.env["document.number.book"].search(
            [
                ("type_id.id", "=", vals['type_id']),
                ("number_format_type", "=", vals['symbol_number_format_type']),
                ("user_id", "=", self.env.uid)
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
        return super(Document, self).write(vals)
    
    def unlink(self):
        for document in self:
            if document.is_public:
                raise ValidationError('Không thể xóa văn bản đã ban hành')
            
            document_book = self.env["document.number.book"].search(
                [
                    ("type_id.id", "=", document.type_id.id),
                    ("number_format_type", "=", document.symbol_number_format_type),
                    ("user_id", "=", self.env.uid)
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
                        ("user_id", "=", self.env.uid)
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
    
    @api.onchange("department_ids")
    def _compute_department_ids(self):
        for document in self:
            if len(document.department_ids) >= 2:
                for department in document.department_ids:
                    if department.code == 'all_department':
                        raise ValidationError('Đơn vị bạn chọn đã bao gồm trong tất cả đơn vị')
                    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=0):
        documents = super(Document, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
        
        for document in documents:
            user_id = document['user_id'][0]
            if user_id != self.env.uid:
                document['can_action_on_document'] = False
            else:
                document['can_action_on_document'] = True
                
            document_read = self.env['document.read'].sudo().search([('document_id', '=', document['id']),('user_id', '=', self.env.uid)], limit=1)
            if document_read:
                document['state_read_document'] = 'done'
                document['is_read_document'] = True
            else:
                document['state_read_document'] = 'new'
                document['is_read_document'] = False
                
        return documents
    
    
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
            'name': 'Văn bản đi',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'document',
            'domain': [('user_id.id', '=', self.env.uid)],
            'limit': 15,
        }
        
        return action
    
    def open_income_document_list(self):
        domain = []
        all_department = self.env['user.info.department'].sudo().search([('code', '=', 'all_department')], limit=1)
        
        if self.env.user.manage_department_id:
            domain.append('|')
            domain.append(('department_ids', 'in', self.env.user.manage_department_id.id))
            domain.append(('department_ids', 'in', all_department.id))
        else:
            dtn = self.env['user.info.department'].sudo().search([('code', '=', 'DTN-HSV')], limit=1)
            domain.append('|')
            domain.append(('department_ids', 'in', dtn.id))
            domain.append(('department_ids', 'in', all_department.id))
            
        domain.append(('is_public', '=', True))
        domain.append(('user_id.id', '!=', self.env.uid))
            
        action = {
            'name': 'Văn bản đến',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'document',
            'view_id': self.env.ref('document_management.income_document_view_tree') .id,
            'domain': domain,
            'limit': 15,
        }
            
        return action;
    
    def public_document(self):
        self.ensure_one()
        
        
        
        self.sudo().write({
            'is_public': True
        })
        
    def cancel_public_document(self):
        self.ensure_one()
        
        self.sudo().write({
            'is_public': False
        })
    
    def mask_as_read_document(self):
        self.ensure_one()
        
        self.env['document.read'].sudo().create({
            'document_id': self.id,
            'user_id': self.env.uid
        })

class DocumenRead(models.Model):
    _name = "document.read"
    _description = "Document Read"
    
    document_id = fields.Many2one('document')
    user_id = fields.Many2one('res.users')
    date_read = fields.Date(string='Ngày đọc', default=fields.Date.context_today)