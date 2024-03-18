from odoo import http
from odoo.http import request
import os
import docx
import base64

class TemporaryController(http.Controller):

    @http.route('/download/document/<string:doc_name>', type='http', auth='user')
    def download_document(self, doc_name):
        # Get the document
        document = request.env['temporary.document'].sudo().search([('name', '=', doc_name)], limit=1)
        if not document:
            return request.not_found()

        # Get the Word file data
        file_data = base64.b64decode(document.word_file)

        # Create a response
        response = http.Response(file_data,
                                 headers=[
                                     ('Content-Disposition', f'attachment; filename="{document.word_filename}"'),
                                     ('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                                 ],
                                 status=200)

        return response
