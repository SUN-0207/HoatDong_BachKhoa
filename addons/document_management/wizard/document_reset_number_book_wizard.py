from odoo import fields, models, api

class DocumentResetNumberBookWizard(models.TransientModel):
    _name = "document.reset.number.book.wizard"
    
    number_format_type = fields.Selection(
        string='Thể thức',
        selection=[('DTN', 'Văn bản Đoàn'), ('HSV', 'Văn bản Hội')]
    )
    
    def reset(self):
        self.ensure_one()
        
        documents = self.env['document'].sudo().search([('user_id','=',self.env.uid),('symbol_number_format_type','=',self.number_format_type)])
        for document in documents:
            if not document.is_public:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thất bại',
                        'message': 'Tồn tại văn bản chưa ban hành',
                        'type': 'danger',
                        'sticky': False,
                    },
                }
                
        document_books = self.env['document.number.book'].sudo().search([('user_id','=',self.env.uid),('number_format_type','=',self.number_format_type)])
        for item in document_books:
            item.sudo().write({
                'current_number_document': 0,
                'current_symbol_number': ''
            })
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Đặt lại thành công, vui lòng đóng cửa sổ',
                'type': 'success',
                'sticky': False,
            },
        }
            
    def close(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {
                'action': {
                    'type': 'ir.actions.act_window_close',
                },
            },
        }