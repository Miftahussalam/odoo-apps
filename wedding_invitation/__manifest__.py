# -*- coding: utf-8 -*-
{
    'name': "Wedding Invitation",

    'summary': """
        Sync data with wedding invitation on https://arin.miftahussalam.com
    """,

    'description': """

    """,

    'author': "Miftahussalam",
    'website': "https://blog.miftahussalam.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Others',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'views/wedding_invitation_menu.xml',
        'views/wedding_wishes_views.xml',
        'views/generate_guest_data_views.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
