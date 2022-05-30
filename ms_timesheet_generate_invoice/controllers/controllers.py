# -*- coding: utf-8 -*-
# from odoo import http


# class MsTimesheetGenerateInvoice(http.Controller):
#     @http.route('/ms_timesheet_generate_invoice/ms_timesheet_generate_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ms_timesheet_generate_invoice/ms_timesheet_generate_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ms_timesheet_generate_invoice.listing', {
#             'root': '/ms_timesheet_generate_invoice/ms_timesheet_generate_invoice',
#             'objects': http.request.env['ms_timesheet_generate_invoice.ms_timesheet_generate_invoice'].search([]),
#         })

#     @http.route('/ms_timesheet_generate_invoice/ms_timesheet_generate_invoice/objects/<model("ms_timesheet_generate_invoice.ms_timesheet_generate_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ms_timesheet_generate_invoice.object', {
#             'object': obj
#         })
