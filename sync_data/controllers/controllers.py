# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WeddingWishes(http.Controller):

    @http.route('/wishes', type='json', auth="none", methods=['POST'], csrf=False)
    def create(self, **post):
        wedding_wishlist_obj = request.env['wedding.wishes'].sudo()
        print('\n post', post)
        return post
