from odoo import models, fields
import docx
import base64
from io import BytesIO

class TemporaryDocument(models.Model):
    _name = 'temporary.document'
    _description = 'Temporary Document'
    
    # File name
    name = fields.Char(string='Name')
    description = fields.Text('Description')
    
    # Purpose
    purpose = fileds.Text('Purpose')
    
    # Require
    require = fields.Text('Require')
    
    # Time
    time = fields.Text('Time')
    
    # Place
    place = fields.Text('Place')
    
    # Object
    object_participant = fields.Text('Object Participant')
    
    # Number of participant
    num_of_participant = fields.Text('Number Of Participant')
    
    # Content
    content = fields.Text('Content')
    
    word_file = fields.Binary('Word File')
    word_filename = fields.Char('Filename')
    
    def generate_word_file(self):
        # Create a new Word document
        doc = docx.Document()

        # Add content to the document
        doc.add_heading('Temporary Document', level=1)
        p = doc.add_paragraph(f"Name: {self.name}")
        doc.add_paragraph(f"Description: {self.description}")   

        # Save the document to a BytesIO object
        byte_io = BytesIO()
        doc.save(byte_io)

        # Convert the BytesIO object to a base64 encoded string
        word_file = base64.b64encode(byte_io.getvalue())

        # Update the record with the Word file and filename
        self.write({
            'word_file': word_file,
            'word_filename': f"{self.name}.docx",
        })
        
    def get_document_url(self):
        self.ensure_one()
        self.generate_word_file()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = f"{base_url}/download/document/{self.name}"
        return {
            'type': 'ir.actions.act_url',
            'url': str(url),
            'target': 'new',
        }
