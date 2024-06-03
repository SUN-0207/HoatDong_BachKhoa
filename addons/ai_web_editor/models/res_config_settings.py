from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    openai_api_key = fields.Char(string="API Key", help="Provide the OpenAI API key here", config_parameter="ai_web_editor.openai_api_key")

    def get_openai_api_key(self):
        return self.env['ir.config_parameter'].sudo().get_param('ai_web_editor.openai_api_key')
