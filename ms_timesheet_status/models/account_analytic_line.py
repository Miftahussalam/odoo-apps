# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _get_is_state_readonly(self):
        for rec in self:
            is_state_readonly = True
            if self.env.user.has_group('hr_timesheet.group_timesheet_manager'):
                is_state_readonly = False
            rec.is_state_readonly = is_state_readonly

    state = fields.Selection([
        ('open', 'Open'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
    ], string='State', default='open')
    is_state_readonly = fields.Boolean(
        string='Is State Readonly',
        compute='_get_is_state_readonly')

    def action_set_to_invoiced(self):
        self.write({'state': 'invoiced'})

    def action_set_to_paid(self):
        self.write({'state': 'paid'})

    def action_set_to_cancel(self):
        self.write({'state': 'cancel'})
