# -*- coding: utf-8 -*-
# from odoo import http


# class MsTimesheetExportExcel(http.Controller):
#     @http.route('/ms_timesheet_export_excel/ms_timesheet_export_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ms_timesheet_export_excel/ms_timesheet_export_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ms_timesheet_export_excel.listing', {
#             'root': '/ms_timesheet_export_excel/ms_timesheet_export_excel',
#             'objects': http.request.env['ms_timesheet_export_excel.ms_timesheet_export_excel'].search([]),
#         })

#     @http.route('/ms_timesheet_export_excel/ms_timesheet_export_excel/objects/<model("ms_timesheet_export_excel.ms_timesheet_export_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ms_timesheet_export_excel.object', {
#             'object': obj
#         })
