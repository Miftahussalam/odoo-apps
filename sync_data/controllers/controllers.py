# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WeddingWishes(http.Controller):

    @http.route('/wishes', type='http', auth="none", methods=['GET'], csrf=False)
    def create(self, **data):
        wedding_wishlist_obj = request.env['wedding.wishes'].sudo()
        print('\n data', data)
        wedding_wishlist_obj.create({
            'name': data.get('name', False),
            'image': data.get('image', False),
            'image_filename': data.get('image_filename', False),
            'description': data.get('description', False),
            'wishes': data.get('wishes', False),
            'invitation_code': data.get('invitation_code', False),
            'invitation_name': data.get('invitation_name', False),
            'invitation_description': data.get('invitation_description', False),
        })
        return 'successfully'
