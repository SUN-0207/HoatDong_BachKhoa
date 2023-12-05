from odoo import fields, models
from odoo.exceptions import UserError, ValidationError

class EventAttendanceCheckWizard(models.TransientModel):
    _name = "event.attendance.check.wizard"
    
    mssv = fields.Char(string="MSSV")