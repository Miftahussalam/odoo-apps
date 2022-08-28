from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from io import BytesIO
from xlrd import open_workbook
import base64
import logging
import json

_logger = logging.getLogger(__name__)


class GenerateGuestData(models.Model):
    _name = "generate.guest.data"
    _description = "Generate Guest Data"

    name = fields.Char(default='New', string='File Name')
    result = fields.Text(
        string="Result",
        required=False)
    file = fields.Binary(string="Excel File", required=True)

    def action_generate(self):
        for rec in self:
            inputx = BytesIO()
            inputx.write(base64.decodestring(rec.file))
            book = open_workbook(file_contents=inputx.getvalue())
            sheets = book.sheets()
            values = []
            for sheet in sheets:
                for i in range(sheet.nrows):
                    if sheet.cell(i, 0).value == 'Kode':
                        continue
                    values.append({
                        "code": sheet.cell(i, 0).value,
                        "name": sheet.cell(i, 1).value,
                        "desc": sheet.cell(i, 2).value,
                        "shift": 1,
                        "isAttended": "",
                        "attendedAt": "",
                        "updatedBy": "",
                        "isExchanged": "",
                        "exchangedAt": "",
                        "exchangedBy": ""
                    })
            print(values)
            rec.result = json.dumps(values, sort_keys=True, indent=4)
