# -*- coding: utf-8 -*-
{
    'name': 'Replenishment Orders',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Automatically generate replenishment orders based on stock levels and reorder rules',
    'description': """
        This module will allow you to create custom reorder rules for products in the system.
        Each product can have a single reordering rule.
        This module uses the scheduled actions to check for the defined rules.
        If any of the rules are to be executed, then immediately a new purchase order is created with required details based on the rule.
        Custom group is added to allow the approval of such orders. Users in the group will be notified via email given the email is configured for the related partner and email server setup is done.
        Such orders cannot be manually confirmed, but only by approving it.
        
        System will periodically check and create the PO as needed.
    """,
    'depends': ['stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/custom_product_reorder_rule_views.xml',
        'views/purchase_order_inherit_views.xml',
        'data/ir_cron.xml',
        'data/mail_template.xml',
    ],
}