# -*- coding: utf-8 -*-
{
    'name': "Timesheet Status",

    'summary': """
        Tracking status of timesheet (open, invoiced, paid, cancel)
    """,

    'description': """

    """,

    'author': "Miftahussalam",
    'website': "https://blog.miftahussalam.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Timesheet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'hr_timesheet',
    ],

    # always loaded
    'data': [
        # 'views/account_analytic_line_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}