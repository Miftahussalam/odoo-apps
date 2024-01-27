# -*- coding: utf-8 -*-
{
    "name": "Timesheet Customer",
    "summary": """
        Customer can login to system and check timesheet for them
    """,
    "description": """

    """,
    "author": "Miftahussalam",
    "website": "https://blog.miftahussalam.com/",
    "category": "Timesheet",
    "version": "17.0.1.0.0",
    "depends": [
        "base",
        "account",
        "product",
        "hr_timesheet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "views/account_analytic_line_views.xml",
    ],
    "demo": [

    ],
    "images": [
        "static/description/images/main_screenshot.png",
    ],
    "license": "LGPL-3",
}
