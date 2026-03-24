from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_payment_state(self):
        super()._compute_payment_state()
        for rec in self.filtered(lambda i: i.timesheet_ids):
            if rec.payment_state in ['in_payment', 'paid']:
                rec.timesheet_ids.write({
                    'state': 'paid',
                })
            elif rec.state != 'cancel':
                rec.timesheet_ids.write({
                    'state': 'invoiced',
                })

    timesheet_ids = fields.One2many(
        comodel_name='account.analytic.line',
        inverse_name='invoice_id',
        string='Timesheets',
        required=False)

    def action_export_to_excel(self):
        self.ensure_one()
        return self.timesheet_ids.action_export_to_excel()

    def button_cancel(self):
        res = super().button_cancel()
        for rec in self.filtered(lambda i: i.timesheet_ids):
            rec.timesheet_ids.write({
                'state': 'open',
            })
        return res

    def button_draft(self):
        res = super().button_draft()
        for rec in self.filtered(lambda i: i.timesheet_ids):
            rec.timesheet_ids.write({
                'state': 'invoiced',
            })
        return res
