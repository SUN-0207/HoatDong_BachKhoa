import logging
import requests
from openai import OpenAI
import google.generativeai as genai

from odoo import http, api, models, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)

class OpenAIModel(http.Controller):
    @http.route(['/fetch_openai_api'], type='json', auth="public")
    def fetch_openai_api(self, question, max_tokens):
        genai.configure(api_key='AIzaSyBAVq9OAVSPXCjMF0_MjHs6k5Smw4GLMcE')
        
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        response = model.generate_content(question)
        
        return response.text