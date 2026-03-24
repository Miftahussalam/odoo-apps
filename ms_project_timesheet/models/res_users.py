from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['action_id'] = self.env.ref('hr_timesheet.timesheet_action_all').id
        return res
