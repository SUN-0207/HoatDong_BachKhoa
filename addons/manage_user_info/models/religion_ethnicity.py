import requests
from odoo import models, fields, api
from .common_constants import *

class UserReligion(models.Model):
    _name = 'user.religion'
    _description = 'Vietnamese Religion'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)

    @api.model
    def init(self):
        for code, name in RELIGION:
            existing_religion = self.env['user.religion'].search([('code', '=', code)], limit=1)
            if not existing_religion:
                self.env['user.religion'].create({
                    'name': name,
                    'code': code,
                })

class UserEthnicity(models.Model):
    _name = 'user.ethnicity'
    _description = 'Vietnamese Ethnicity'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)

    @api.model
    def init(self):
        for code, name in ETHNICITY:
            existing_ethnicity = self.env['user.ethnicity'].search([('code', '=', code)], limit=1)
            if not existing_ethnicity:
                self.env['user.ethnicity'].create({
                    'name': name,
                    'code': code,
                })

