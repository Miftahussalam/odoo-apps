# -*- coding: utf-8 -*-
from odoo import http

# class MsTimesheetStatus(http.Controller):
#     @http.route('/ms_timesheet_status/ms_timesheet_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ms_timesheet_status/ms_timesheet_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ms_timesheet_status.listing', {
#             'root': '/ms_timesheet_status/ms_timesheet_status',
#             'objects': http.request.env['ms_timesheet_status.ms_timesheet_status'].search([]),
#         })

#     @http.route('/ms_timesheet_status/ms_timesheet_status/objects/<model("ms_timesheet_status.ms_timesheet_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ms_timesheet_status.object', {
#             'object': obj
#         })