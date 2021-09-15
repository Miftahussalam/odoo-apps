# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    state = fields.Selection([
        ('open','Open'),
        ('invoiced','Invoiced'),
        ('paid','Paid'),
        ('cancel','Cancel'),
    ], string='State', default='open')

    @api.multi
    def action_set_to_invoiced(self):
        self.write({'state':'invoiced'})

    @api.multi
    def action_set_to_paid(self):
        self.write({'state':'paid'})

    @api.multi
    def action_set_to_cancel(self):
        self.write({'state':'cancel'})
