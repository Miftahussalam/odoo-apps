from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_freeze = fields.Boolean(string='Is Freeze?', copy=False)
