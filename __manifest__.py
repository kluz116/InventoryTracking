# -*- coding: utf-8 -*-
{
    'name': "Inventory Tracker",

    'summary': "Application To Track Inventories",

    'description': "This is an Inventory Tracker application developed with Python Odoo Framework for ERPS",
    'author': "Finance Trust Bank",
    'website': "http://www.financetrust.co.ug",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '0.1',
    
    # any module necessary for this one to work correctly
    'depends': ['mail','base'],
  
    # always loaded
    'data': [
        
        'security/inventory_security.xml',
        'security/ir.model.access.csv',
        #'data/email_template_cash_managment.xml',
        'wizard/verify_asset.xml',
        'views/inventory.xml',
        'views/configs.xml',
        
       

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}