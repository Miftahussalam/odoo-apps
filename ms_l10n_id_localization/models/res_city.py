from odoo import fields, models


class ResCity(models.Model):
    # res.city sudah didefinisikan base_address_extended (name, zipcode,
    # country_id, state_id dengan domain per-country). Dulu modul ini pakai
    # _name baru (Odoo diam-diam menggabung field dari dua _name yang sama,
    # mirip _inherit implisit) - begitu base_address_extended ikut terinstall
    # (jadi dependency contacts/portal di Odoo 20), state_id kita (domain=[],
    # required=True) rebutan sama punya core (domain per country_id),
    # bikin crash "Unknown field res.city.country_id". _inherit eksplisit di
    # sini biar jelas ini nambahin field, bukan field kita yang menang.
    _inherit = "res.city"

    subdistrict_ids = fields.One2many(
        comodel_name='res.subdistrict',
        inverse_name='city_id',
        string='Kecamatan',
        readonly=True)
