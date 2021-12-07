# -*- coding: utf-8 -*-

{
    'name': 'Product Stock Xls Report',
    'version': '3.5',
    'category': 'HR',
    'summary': 'Product Stock Xls Report',
    'author': "Silla",
    'description': """
        Product Stock Xls Report
    """,
    'depends': ['report_xlsx', 'stock'],
    'data': [
        'views/product_stock.xml'
    ],
    'qweb': [],
    'application': True,
}
