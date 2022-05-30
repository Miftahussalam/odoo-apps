# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def action_export_to_excel(self):
        pass
