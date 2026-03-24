{
    "name": "Project Timesheet",
    "summary": """
        Enhanced project timesheet with start/stop tracking, start-end time logging, excel export, etc
    """,
    "description": """
    """,
    "author": "Miftahussalam",
    "website": "https://blog.miftahussalam.com/",
    "category": "Services/Timesheets",
    "version": "19.0.1.0.0",
    "depends": [
        "base",
        "mail",
        "account",
        "project",
        "analytic",
        "hr_timesheet",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
        "views/res_partner_views.xml",
        "views/hr_employee_views.xml",
        "views/res_users_views.xml",
        "views/report_invoice.xml",
    ],
    "demo": [

    ],
    "images": [

    ],
    "license": "LGPL-3",
}
