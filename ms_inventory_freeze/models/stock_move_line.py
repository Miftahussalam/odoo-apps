from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _action_done(self):
        for rec in self:
            if not rec.move_id.inventory_id:
                if rec.location_id.freeze_status == 'full':
                    raise ValidationError(
                        "Can't move product %s from location %s, because the location is in fully freeze status. "
                        "Stock move can be process after inventory adjustment done" % (
                            rec.product_id.display_name, rec.location_id.display_name
                        )
                    )
                elif rec.location_dest_id.freeze_status == 'full':
                    raise ValidationError(
                        "Can't move product %s to location %s, because the location is in fully freeze status. "
                        "Stock move can be process after inventory adjustment done" % (
                            rec.product_id.display_name,rec.location_dest_id.display_name)
                    )
                elif rec.location_id.freeze_status and rec.product_id.is_freeze:
                    raise ValidationError(
                        "Can't move product %s from location %s, because the product and location is in freeze status. "
                        "Stock move can be process after inventory adjustment done" % (
                            rec.product_id.display_name, rec.location_id.display_name)
                    )
                elif rec.location_dest_id.freeze_status and rec.product_id.is_freeze:
                    raise ValidationError(
                        "Can't move product %s to location %s, because the product and location is in freeze status. "
                        "Stock move can be process after inventory adjustment done" % (
                            rec.product_id.display_name, rec.location_dest_id.display_name)
                    )
        return super(StockMoveLine, self)._action_done()
    