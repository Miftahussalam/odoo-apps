from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    timesheet_ids = fields.One2many(
        comodel_name='account.analytic.line',
        inverse_name='invoice_id',
        string='Timesheets',
        required=False)
