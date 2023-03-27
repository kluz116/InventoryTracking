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

    'external_dependencies': {
        'python': [
            'xlsxwriter',
            'xlrd',
        ],
    },
    
    # any module necessary for this one to work correctly
    'depends': ['mail','base'],
  
    # always loaded
    'data': [
        
        'security/inventory_security.xml',
        'security/ir.model.access.csv',
        'data/email_template_inventory.xml',
        'data/ir_cron_data.xml',
        'wizard/verify_asset.xml',
        'wizard/dispatch_asset.xml',
        'wizard/verify_asset_one.xml',
        'wizard/activate_asset.xml',
        'wizard/stock_asset.xml',
        'wizard/reject_asset.xml',
        'wizard/reject_admin.xml',
        'wizard/approve_asset.xml',
        'wizard/approve_admin.xml',
        'wizard/repair_asset.xml',
        'wizard/dispose_asset.xml',
        'wizard/approve.xml',
        'wizard/initiate_diagnosis.xml',
        'wizard/diagnosis.xml',
        'wizard/initiate_repair.xml',
        'wizard/internal_initiate_repair.xml',
        'wizard/infra_approve_deployment.xml',
        'wizard/infra_reject_deployment.xml',
        'wizard/verify_asset_reject.xml',
        'wizard/approve_repair.xml',
        'wizard/reject_repair.xml',
        'views/inventory.xml',
        'views/configs.xml',
        'views/inventory_user.xml',
        'reports/report_inventoryTracking.xml',
        'reports/asset_transfer.xml',
        'reports/assest_checklist.xml',
        
    
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}