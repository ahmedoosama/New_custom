# -*- coding: utf-8 -*-

{
    'name': 'Point of Sale Data Cache',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Webveer',
    'summary': 'This module reduce POS data loading time. 10000 Products and  10000 Customers will load within 3 or 4  Sec.',
    'description': """

=======================

This module reduce POS data loading time. 10000 Products and  10000 Customers will load within 3 or 4  Sec.

""",
    'depends': ['pos_cache'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'qweb': [
        # 'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/pos.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 99,
    'currency': 'EUR',
}
