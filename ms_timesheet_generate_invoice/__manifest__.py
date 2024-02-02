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
    "version": "13.0.1.0.0",
    "depends": [
        "base",
        "account",
        "analytic",
        "hr_timesheet",
        "ms_timesheet_partner",
        "ms_timesheet_start_stop",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
    ],
    "demo": [

    ],
}
