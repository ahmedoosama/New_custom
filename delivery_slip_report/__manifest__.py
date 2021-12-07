# -*- coding: utf-8 -*-
{
    'name': "Print Delivery slip",

    'summary': """
        On Hand Qty Group
        """,

    'description': """
        Print Delivery Slip
    """,

    'author': "Silla Tech",
    'website': 'sillatech.net',


    'category': 'Inventory',
    'version': '0.1',

    'depends': ['silla_inventory'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
