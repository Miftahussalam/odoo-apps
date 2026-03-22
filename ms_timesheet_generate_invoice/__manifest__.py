# -*- coding: utf-8 -*-
{
    "name": "Timesheet Generate Invoice",
    "summary": """
        Generate customer invoice based on timesheet
    """,
    "description": """

    """,
    "author": "Miftahussalam",
    "website": "https://blog.miftahussalam.com/",
    "category": "Timesheet",
    "version": "19.0.1.0.0",
    "depends": [
        "base",
        "account",
        "analytic",
        "hr_timesheet",
        "ms_timesheet_partner",
        "ms_timesheet_start_stop",
    ],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
        "views/res_partner_views.xml",
        "views/report_invoice.xml",
    ],
    "demo": [

    ],
}
