from odoo import http
from odoo.http import request

class CustomLoginAdmin(http.Controller):

    @http.route('/web/login/admin', type='http', auth="public", website=True)
    def custom_login_page(self, **kw):
        return request.render('code_backend_theme.custom_login_admin', {})