# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from io import BytesIO
import pytz
import xlsxwriter
import base64
from datetime import datetime, date
from pytz import timezone

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone('Asia/Jakarta'))

    file_data = fields.Binary('File', readonly=True)
    
    def cell_format(self, workbook):
        cell_format = {}
        cell_format['title'] = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 20,
            'font_name': 'Arial',
        })
        cell_format['no'] = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })
        cell_format['header'] = workbook.add_format({
            'bold': True,
            'align': 'center',
            'bg_color': '#d9d9d9',
            'border': True,
            'font_name': 'Arial',
        })
        cell_format['content'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'font_name': 'Arial',
        })
        cell_format['content_float'] = workbook.add_format({
            'font_size': 11,
            'border': True,
            'num_format': '#,##0.00',
            'font_name': 'Arial',
        })
        cell_format['total'] = workbook.add_format({
            'bold': True,
            'bg_color': '#d9d9d9',
            'num_format': '#,##0.00',
            'border': True,
            'font_name': 'Arial',
        })
        return cell_format, workbook

    def action_export_to_excel(self):
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        cell_format, workbook = self.cell_format(workbook)
        report_name = 'Timesheet'
        worksheet = workbook.add_worksheet()
        columns = [
            'Date',
            'Description',
            'Start Time',
            'End Time',
            'Duration (Hour(s))',
        ]
        column_length = len(columns)
        if not column_length:
            return False
        no = 1
        column = 1

        worksheet.set_column('A:A', 6)
        worksheet.set_column(1, column_length, 30)
        worksheet.merge_range(0, 0, 1, column_length, report_name, cell_format['title'])
        worksheet.write('A4', 'No', cell_format['header'])

        for col in columns:
            worksheet.write(3, column, col, cell_format['header'])
            column += 1
        data_list = []
        for rec in self:
            data_list.append([
                rec.date,
                rec.name,
                rec.start_time,
                rec.end_time,
                rec.unit_amount,
            ])
        row = 5
        column_float_number = {}
        for data in data_list:
            worksheet.write('A%s' % row, no, cell_format['no'])
            no += 1
            column = 1
            for value in data:
                if type(value) is int or type(value) is float:
                    content_format = 'content_float'
                    column_float_number[column] = column_float_number.get(column, 0) + value
                else:
                    content_format = 'content'
                if isinstance(value, datetime):
                    value = pytz.UTC.localize(value).astimezone(timezone(self.env.user.tz or 'UTC'))
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')
                worksheet.write(row - 1, column, value, cell_format[content_format])
                column += 1
            row += 1

        row -= 1
        for x in range(column_length + 1):
            if x == 0:
                worksheet.write('A%s' % (row + 1), 'Total', cell_format['header'])
            elif x not in column_float_number:
                worksheet.write(row, x, '', cell_format['header'])
            else:
                worksheet.write(row, x, column_float_number[x], cell_format['total'])

        workbook.close()
        result = base64.encodestring(fp.getvalue())
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        filename = '%s %s' % (report_name, date_string)
        filename += '%2Exlsx'
        self.write({'file_data': result})
        url = "web/content/?model=" + self._name + "&id=" + str(
            self[:1].id) + "&field=file_data&download=true&filename=" + filename
        return {
            'name': 'Generic Excel Report',
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
