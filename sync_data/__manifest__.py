# -*- coding: utf-8 -*-
{
    'name': "Sync Data",

    'summary': """
        Sync data from other apps, instance, machine, dll
    """,

    'description': """

    """,

    'author': "Miftahussalam",
    'website': "https://blog.miftahussalam.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sync',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
    ],

    # always loaded
    'data': [
        'views/sync_data_views.xml',
        'views/wedding_wishlist_views.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
