from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = 'stock.location'

    freeze_status = fields.Selection([
        ('full', 'Fully Freeze'),
        ('partial', 'Partially Freeze'),
    ], string='Freeze Status', copy=False)
