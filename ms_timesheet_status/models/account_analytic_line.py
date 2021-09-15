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
