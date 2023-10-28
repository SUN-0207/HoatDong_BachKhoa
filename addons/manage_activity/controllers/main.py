import babel.dates
import pytz
import re
import werkzeug

from ast import literal_eval
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from werkzeug.datastructures import OrderedMultiDict
from werkzeug.exceptions import NotFound

from odoo import fields, http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.osv import expression
from odoo.tools.misc import get_lang
from odoo.tools import lazy
from odoo.exceptions import UserError, AccessError, MissingError 

from odoo.addons.website_event.controllers.main import WebsiteEventController

class WebsitEventCustomController(WebsiteEventController):
    
    @http.route('/event/check_user_registration', type='json', auth='public')
    def check_user_registration(self, event_id=None, partner_id=None):
        if event_id and partner_id:
            event = request.env['event.event'].sudo().browse(int(event_id))
            partner = request.env['res.partner'].sudo().browse(int(partner_id))

            if event and partner:
                registration = request.env['event.registration'].sudo().search_count([
                    ('event_id', '=', event.id),
                    ('partner_id', '=', partner.id)
                ])

                is_registered = bool(registration)

                return {'is_registered': is_registered}

        return {'is_registered': False}
        
    def _process_tickets_form_inherit(self, event, form_details):
        """ Process posted data about ticket order. Generic ticket are supported
        for event without tickets (generic registration).

        :return: list of order per ticket: [{
            'id': if of ticket if any (0 if no ticket),
            'ticket': browse record of ticket if any (None if no ticket),
            'name': ticket name (or generic 'Registration' name if no ticket),
            'quantity': number of registrations for that ticket,
        }, {...}]
        """
        ticket_order = {}
        selected_ticket_id = None
        print(form_details)
        for key, value in form_details.items():
            print("*********************** Key: ", key)
            print("*********************** Key: ", value)
            registration_items = key.split('nb_register-')
            if len(registration_items) != 2:
                continue
            ticket_id = int(registration_items[1])
            if int(value) > 0:
                selected_ticket_id = ticket_id
            ticket_order[ticket_id] = int(value)

        ticket_dict = {}
        if selected_ticket_id:
            selected_ticket = request.env['event.event.ticket'].sudo().search([
                ('id', '=', selected_ticket_id),
                ('event_id', '=', event.id)
            ])
            if selected_ticket:
                ticket_dict[selected_ticket.id] = selected_ticket

        return [{
            'id': tid if ticket_dict.get(tid) else 0,
            'ticket': ticket_dict.get(tid),
            'name': ticket_dict[tid]['name'] if ticket_dict.get(tid) else _('Registration'),
            'quantity': count,
        } for tid, count in ticket_order.items() if count]

    @http.route(['/event/<model("event.event"):event>/registration/new'], type='json', 
        auth="public", methods=['POST'], website=True)
    def registration_new(self, event, **post):
        availability_check = True
        # Check if the user has already registered for the event
        user_registered = request.env['event.registration'].sudo().search_count([
            ('event_id', '=', event.id),
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        if user_registered:
            availability_check = False
        #load data for form
        tickets = self._process_tickets_form_inherit(event, post)
        
        if event.seats_limited:
            ordered_seats = 0
            for ticket in tickets:
                ordered_seats += ticket['quantity']
            if event.seats_available < ordered_seats:
                availability_check = False
        if not tickets:
            return False
        
        #load data for form
        default_first_attendee = {}
        if not request.env.user._is_public():
            default_first_attendee = {
                "name": request.env.user.name,
                "email": request.env.user.email,
                "phone": request.env.user.user_info_id.phone_number,
                "gender": request.env.user.user_info_id.gender 
            }
    
        return request.env['ir.ui.view']._render_template("website_event.registration_attendee_details", {
            'tickets': tickets,
            'event': event,
            'availability_check': availability_check,
            'default_first_attendee': default_first_attendee,
        })
    
    def _process_attendees_form(self, event, form_details):
        """ Process data posted from the attendee details form.

        :param form_details: posted data from frontend registration form, like
            {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
        """
        allowed_fields = request.env['event.registration']._get_website_registration_allowed_fields()
        registration_fields = {key: v for key, v in request.env['event.registration']._fields.items() if key in allowed_fields}
        for ticket_id in list(filter(lambda x: x is not None, [form_details[field] if 'event_ticket_id' in field else None for field in form_details.keys()])):
            if int(ticket_id) not in event.event_ticket_ids.ids and len(event.event_ticket_ids.ids) > 0:
                raise UserError(_("This ticket is not available for sale for this event"))
        registrations = {}
        global_values = {}
        for key, value in form_details.items():
            counter, attr_name = key.split('-', 1)
            field_name = attr_name.split('-')[0]
            if field_name not in registration_fields:
                continue
            elif isinstance(registration_fields[field_name], (fields.Many2one, fields.Integer)):
                value = int(value) or False  # 0 is considered as a void many2one aka False
            else:
                value = value

            if counter == '0':
                global_values[attr_name] = value
            else:
                registrations.setdefault(counter, dict())[attr_name] = value
        for key, value in global_values.items():
            for registration in registrations.values():
                registration[key] = value

        return list(registrations.values())

    def _create_attendees_from_registration_post(self, event, registration_data):
        """ Also try to set a visitor (from request) and
        a partner (if visitor linked to a user for example). Purpose is to gather
        as much informations as possible, notably to ease future communications.
        Also try to update visitor informations based on registration info. """
        visitor_sudo = request.env['website.visitor']._get_visitor_from_request(force_create=True)

        registrations_to_create = []
        for registration_values in registration_data:
            registration_values['event_id'] = event.id
            if not registration_values.get('partner_id') and visitor_sudo.partner_id:
                registration_values['partner_id'] = visitor_sudo.partner_id.id
            elif not registration_values.get('partner_id'):
                registration_values['partner_id'] = False if request.env.user._is_public() else request.env.user.partner_id.id

            # update registration based on visitor
            registration_values['visitor_id'] = visitor_sudo.id

            registrations_to_create.append(registration_values)

        return request.env['event.registration'].sudo().create(registrations_to_create)

    @http.route(['''/event/<model("event.event"):event>/registration/confirm'''], type='http', auth="public", methods=['POST'], website=True)
    def registration_confirm(self, event, **post):
        registrations = self._process_attendees_form(event, post)
        attendees_sudo = self._create_attendees_from_registration_post(event, registrations)

        return request.redirect(('/event/%s/registration/success?' % event.id) + werkzeug.urls.url_encode({'registration_ids': ",".join([str(id) for id in attendees_sudo.ids])}))
