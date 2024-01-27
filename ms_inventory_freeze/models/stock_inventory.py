from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def action_start(self):
        res = super(StockInventory, self).action_start()
        for inventory in self:
            location_ids = self.env['stock.location'].search([
                ('id', 'child_of', inventory.location_ids.ids)
            ])
            if not location_ids:
                location_ids = self.env['stock.location'].search([
                    ('usage', '=', 'internal')
                ])
            product_ids = inventory.product_ids
            if not product_ids:
                product_ids = self.env['product.product'].search([])
            product_ids.write({'is_freeze':True})
            if not inventory.product_ids:
                location_ids.write({'freeze_status': 'full'})
            else:
                location_ids.write({'freeze_status': 'partial'})
        return res
    prepare_inventory = action_start

    def set_freeze_false(self):
        for inventory in self:
            location_ids = self.env['stock.location'].search([
                ('id', 'child_of', inventory.location_ids.ids)
            ])
            if not location_ids:
                location_ids = self.env['stock.location'].search([
                    ('usage', '=', 'internal')
                ])
            location_ids.write({'freeze_status': False})
            product_ids = inventory.product_ids
            if not product_ids:
                product_ids = self.env['product.product'].search([])
            product_ids.write({'is_freeze': False})

    def action_cancel_draft(self):
        res = super(StockInventory, self).action_cancel_draft()
        self.set_freeze_false()
        return res

    def _action_done(self):
        res = super(StockInventory, self)._action_done()
        self.set_freeze_false()
        return res
    