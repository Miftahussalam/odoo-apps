from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class WeddingWishes(models.Model):
    _name = "wedding.wishes"
    _description = "Wedding Wishes"
    _order = "id desc"

    name = fields.Char(string='Name')
    image = fields.Binary(string="image")
    image_filename = fields.Char(string="Image Filename")
    description = fields.Char(
        string='Description', 
        required=False)
    wishes = fields.Text(
        string="Wishes",
        required=False)
    invitation_code = fields.Char(
        string='Code',
        required=False)
    invitation_name = fields.Char(
        string='Name',
        required=False)
    invitation_description = fields.Char(
        string='Description',
        required=False)
