# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class WeddingWishes(http.Controller):

    @http.route('/wishes', type='http', auth="none", methods=['GET'], csrf=False)
    def create(self, **data):
        wedding_wishlist_obj = request.env['wedding.wishes'].sudo()
        vals = {
            'name': data.get('name', False),
            'image_filename': data.get('image_filename', '').replace('undefined', '').split('\\')[-1],
            'description': data.get('description', False),
            'wishes': data.get('wishes', False),
            'invitation_code': data.get('invitation_code', False),
            'invitation_name': data.get('invitation_name', False),
            'invitation_description': data.get('invitation_description', False),
        }
        if data.get('image', 'undefined') not in ['undefined']:
            if type(data['image']) == str and 'base64' in data['image']:
                image_vals = data['image'].split('base64,')
                vals['image'] = image_vals[-1]
        wedding_wishlist_obj.create(vals)
        return 'successfully'

    def get_token(self, type=False):
        criteria = []
        if type:
            criteria.append(('type', '=', type))
        token_id = http.request.env['ms.telegram.token'].search(criteria, limit=1)
        if not token_id:
            ValidationError(_('Token not found.'))
        return f'bot{token_id.name}'

    @http.route('/telegram/webhook/receiver', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **post):
        token = '6766364282:AAGzV6Lpy6Aj3BN2RD8JRM-CnVETF_ACZwE'  # self.get_token()
        payload = json.loads(http.request.httprequest.data)
        _logger.info(f"payload: {payload}")
        _logger.info(f"post: {post}")
        message = "Pesan anda telah kami terima. Terimaksih"
        chat_id = payload['message']['chat']['id']
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        data = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=data)
        _logger.info(f"response: {response.json()}")
