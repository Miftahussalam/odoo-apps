# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def action_generate_invoice(self):
        project_ids = self.mapped('project_id')
        no_customer_project_ids = project_ids.filtered(lambda p: not p.partner_id)
        if no_customer_project_ids:
            raise ValidationError(_(f'Please set customer for project: {", ".join(no_customer_project_ids.mapped("name"))}'))
        no_price_project_ids = project_ids.filtered(lambda p: not p.price_unit)
        if no_price_project_ids:
            raise ValidationError(_(f'Please set price unit per hour for project: {", ".join(no_price_project_ids.mapped("name"))}'))
        partner_ids = project_ids.mapped('partner_id')
        invoice_ids = self.env['account.move']
        for partner_id in partner_ids:
            line_vals = []
            partner_project_ids = project_ids.filtered(lambda p: p.partner_id == partner_id)
            for project_id in partner_project_ids:
                timesheet_ids = self.filtered(lambda t: t.project_id == project_id)
                line_vals.append((0, 0, {
                    'name': f'Custom module {project_id.display_name}',
                    'quantity': round(sum(l.unit_amount for l in timesheet_ids), 2),
                    'price_unit': project_id.price_unit,
                    'tax_ids': [],
                }))
            invoice_id = self.env['account.move'].create({
                'partner_id': partner_id.id,
                'type': 'out_invoice',
                'invoice_line_ids': line_vals
            })
            invoice_id.action_post()
            invoice_ids += invoice_id
        self.write({'state':'invoiced'})
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
