from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_signature = fields.Boolean(
        string='Invoice With Signature',
        required=False)
