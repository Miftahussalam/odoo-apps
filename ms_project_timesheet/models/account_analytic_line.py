# -*- coding: utf-8 -*-


import pytz
import xlsxwriter
import base64
from odoo import models, fields, api, _
from io import BytesIO
from datetime import datetime, date, timedelta
from pytz import timezone
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    _order = 'start_time DESC'

    @api.model
    def get_default_date_tz(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone('Asia/Jakarta'))

    @api.depends('project_id.price_unit', 'employee_id.timesheet_cost', 'unit_amount', 'date')
    def _get_amount(self):
        for rec in self:
            amount = round(rec.project_id.price_unit * rec.unit_amount, -3)
            developer_amount = round(rec.employee_id.timesheet_cost * rec.unit_amount, -3)
            target_amount = 0
            if rec.date:
                timesheet_target_amount = self.env['ir.config_parameter'].sudo().get_param('timesheet_target_amount',
                                                                                           '0')
                timesheet_target_amount = float(timesheet_target_amount)
                current_date = rec.date
                current_month = rec.date.month
                while current_date.month == current_month:
                    if current_date.weekday() <= 4:
                        target_amount += timesheet_target_amount
                    current_date = current_date - timedelta(days=1)
            rec.amount = amount
            rec.developer_amount = developer_amount
            rec.real_amount = amount - developer_amount
            rec.target_amount = target_amount

    @api.depends('start_time', 'end_time', 'break_time', 'break_unit_amount')
    def _get_unit_amount(self):
        for rec in self:
            unit_amount = 0
            if rec.start_time and (rec.break_time or rec.end_time):
                if rec.end_time:
                    unit_amount = rec.end_time - rec.start_time
                else:
                    unit_amount = rec.break_time - rec.start_time
                unit_amount = unit_amount.total_seconds() / 60 / 60
                if rec.break_unit_amount:
                    unit_amount -= rec.break_unit_amount
            rec.unit_amount = unit_amount

    def _get_is_state_readonly(self):
        for rec in self:
            is_state_readonly = True
            if self.env.user.has_group('hr_timesheet.group_timesheet_manager'):
                is_state_readonly = False
            rec.is_state_readonly = is_state_readonly

    @api.depends(
        'start_time',
        'employee_id',
    )
    def _compute_date(self):
        for rec in self:
            rec.date = False
            if rec.start_time:
                tz = rec.employee_id.tz or 'Asia/Jakarta'
                local_dt = fields.Datetime.context_timestamp(
                    rec.with_context(tz=tz),
                    rec.start_time
                )
                rec.date = local_dt.date()

    file_data = fields.Binary('File', readonly=True)
    amount = fields.Float(
        string='Amount',
        store=True,
        compute='_get_amount')
    developer_amount = fields.Float(compute='_get_amount', string='Developer Amount', store=True)
    real_amount = fields.Float(compute='_get_amount', string='Real Amount', store=True)
    target_amount = fields.Float(compute='_get_amount', string='Target Amount', store=True)
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    break_time = fields.Datetime(
        string='Break Time',
        readonly=True,
        copy=False)
    break_unit_amount = fields.Float(string='Break Time (Hour(s))')
    unit_amount = fields.Float(compute='_get_unit_amount', store=True)
    state = fields.Selection([
        ('open', 'Open'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
    ], string='State', default='open', copy=False)
    is_state_readonly = fields.Boolean(
        string='Is State Readonly',
        compute='_get_is_state_readonly')
    invoice_id = fields.Many2one(
        comodel_name='account.move',
        string='Invoice',
        copy=False)
    date = fields.Date(
        compute='_compute_date',
        compute_sudo=True,
        store=True,
        required=False,
    )

    def default_get(self, fields_list):
        self = self.with_context(default_project_id=False)
        res = super(AccountAnalyticLine, self).default_get(fields_list)
        res['project_id'] = False
        return res

    def action_generate_invoice(self):
        invalid_records = self.filtered(lambda r: r.state != 'open')
        if invalid_records:
            raise ValidationError(_(
                "You can only generate invoices for timesheets that are in 'Open' status."
            ))
        invalid_records = self.filtered(lambda r: r.amount <= 0)
        if invalid_records:
            raise ValidationError(_(
                "You can only generate invoices for timesheets that have a valid amount."
            ))
        project_ids = self.mapped('project_id')
        no_customer_project_ids = project_ids.filtered(lambda p: not p.partner_id)
        if no_customer_project_ids:
            raise ValidationError(
                _(f'Please set customer for project: {", ".join(no_customer_project_ids.mapped("name"))}'))
        no_price_project_ids = project_ids.filtered(lambda p: not p.price_unit)
        if no_price_project_ids:
            raise ValidationError(
                _(f'Please set price unit per hour for project: {", ".join(no_price_project_ids.mapped("name"))}'))
        partner_ids = project_ids.mapped('partner_id')
        invoice_ids = self.env['account.move']
        for partner_id in partner_ids:
            line_vals = []
            partner_project_ids = project_ids.filtered(lambda p: p.partner_id == partner_id)
            partner_timesheet_ids = self.env['account.analytic.line']
            for project_id in partner_project_ids:
                timesheet_ids = self.filtered(lambda t: t.project_id == project_id)
                partner_timesheet_ids |= timesheet_ids
                line_vals.append((0, 0, {
                    'name': f'Custom module {project_id.display_name}',
                    'quantity': round(sum(l.unit_amount for l in timesheet_ids), 2),
                    'price_unit': project_id.price_unit,
                    'tax_ids': [],
                }))
            narration = ''
            if self.env.user.company_id.partner_id.bank_ids:
                bank_list = [f'{bank_id.bank_id.name} {bank_id.acc_number}' for bank_id in
                             self.env.user.company_id.partner_id.bank_ids]
                bank_list = '<br/>'.join(bank_list)
                narration = f"{bank_list}<br/><br/>a/n {self.env.user.company_id.name}"
            invoice_id = self.env['account.move'].create({
                'partner_id': partner_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': line_vals,
                'narration': narration,
                'partner_bank_id': False,
            })
            partner_timesheet_ids.write({
                'invoice_id': invoice_id.id
            })
            invoice_id.action_post()
            invoice_ids += invoice_id
        self.write({'state': 'invoiced'})
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoice_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': invoice_ids.id,
                'views': [[False, 'form']]
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', invoice_ids.ids)],
            })
        return action

    def action_view_invoice(self):
        invoice_ids = self.mapped('invoice_id')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoice_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': invoice_ids.id,
                'views': [[False, 'form']]
            })
        else:
            action.update({
                'view_mode': 'list,form',
                'domain': [('id', 'in', invoice_ids.ids)],
            })
        return action

    def recalculate_amount(self):
        rec_ids = self.search([
            ('amount', 'in', [0, False]),
            ('project_id.price_unit', '!=', 0),
        ])
        rec_ids._get_amount()
    
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
            'border': True,
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
        project_ids = self.mapped('project_id')
        for project_id in project_ids:
            worksheet = workbook.add_worksheet(project_id.name)
            columns = [
                'Date',
                'Description',
                'Start Time',
                'End Time',
                'Break Time (Hour(s))',
                'Duration (Hour(s))',
            ]
            column_length = len(columns)
            if not column_length:
                return False
            no = 1
            column = 1

            worksheet.set_column('A:A', 5)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 80)
            worksheet.set_column('D:G', 20)
            worksheet.merge_range(0, 0, 1, column_length, report_name, cell_format['title'])
            worksheet.write('A4', 'No', cell_format['header'])

            for col in columns:
                worksheet.write(3, column, col, cell_format['header'])
                column += 1
            data_list = []
            for rec in self.filtered(lambda t: t.project_id == project_id).sorted(key=lambda t: t.start_time):
                data_list.append([
                    rec.date or '',
                    rec.name or '',
                    rec.start_time or '',
                    rec.end_time or '',
                    rec.break_unit_amount or 0,
                    rec.unit_amount or 0,
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
        result = base64.b64encode(fp.getvalue())
        datetime_string = self.get_default_date_tz().strftime("%Y-%m-%d %H:%M:%S")
        filename = '%s %s' % (report_name, datetime_string)
        filename += '%2Exlsx'
        self.write({'file_data': result})
        url = "web/content/?model=" + self._name + "&id=" + str(
            self[:1].id) + "&field=file_data&download=true&filename=" + filename
        return {
            'name': 'Timesheets',
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    def button_start_stop(self):
        for rec in self.filtered(lambda t: not t.break_time):
            if not rec.start_time:
                rec.write({
                    'start_time': fields.Datetime.now(),
                })
            elif not rec.end_time:
                rec.write({
                    'end_time': fields.Datetime.now(),
                })

    def button_break_resume(self):
        for rec in self.filtered(lambda t: t.start_time and not t.end_time):
            if not rec.break_time:
                rec.write({
                    'break_time': fields.Datetime.now(),
                })
            else:
                additional_break = fields.Datetime.now() - rec.break_time
                additional_break = additional_break.total_seconds() / 3600.0
                rec.write({
                    'break_time': False,
                    'break_unit_amount': rec.break_unit_amount + additional_break
                })

    @api.constrains('end_time')
    def _check_break_time(self):
        for rec in self:
            if rec.end_time and rec.break_time:
                raise ValidationError(_(f'Please click button resume first for timesheet {rec.display_name}.'))

    def action_set_to_open(self):
        self.write({'state': 'open'})

    def action_set_to_invoiced(self):
        self.write({'state': 'invoiced'})

    def action_set_to_paid(self):
        self.write({'state': 'paid'})

    def action_set_to_cancel(self):
        self.write({'state': 'cancel'})

    def unlink(self):
        invalid_records = self.filtered(lambda r: r.state != 'open')
        if invalid_records:
            raise ValidationError(_(
                "You can only delete records that are in 'Open' state."
            ))
        return super().unlink()
