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
    "version": "16.0.1.0.0",
    "depends": [
        "base",
        "account",
        "product",
        "hr_timesheet",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/account_analytic_line_views.xml",
    ],
    "demo": [

    ],
    "license": "AGPL-3",
}
