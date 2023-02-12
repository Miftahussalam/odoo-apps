# -*- coding: utf-8 -*-
# from odoo import http


# class MsTimesheetPartner(http.Controller):
#     @http.route('/ms_timesheet_partner/ms_timesheet_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ms_timesheet_partner/ms_timesheet_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ms_timesheet_partner.listing', {
#             'root': '/ms_timesheet_partner/ms_timesheet_partner',
#             'objects': http.request.env['ms_timesheet_partner.ms_timesheet_partner'].search([]),
#         })

#     @http.route('/ms_timesheet_partner/ms_timesheet_partner/objects/<model("ms_timesheet_partner.ms_timesheet_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ms_timesheet_partner.object', {
#             'object': obj
#         })
