# -*- coding: utf-8 -*-
# from odoo import http


# class SyncData(http.Controller):
#     @http.route('/sync_data/sync_data/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sync_data/sync_data/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sync_data.listing', {
#             'root': '/sync_data/sync_data',
#             'objects': http.request.env['sync_data.sync_data'].search([]),
#         })

#     @http.route('/sync_data/sync_data/objects/<model("sync_data.sync_data"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sync_data.object', {
#             'object': obj
#         })
