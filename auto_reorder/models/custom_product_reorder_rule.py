# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class CustomProductReorderRule(models.Model):
    _name = 'custom.product.reorder.rule'
    _description = 'Product Reorder Rule'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    min_qty = fields.Float(string='Minimum Quantity', required=True)
    reorder_qty = fields.Float(string='Reorder Quantity', required=True)
    lead_time = fields.Integer(string='Lead Time (days)', required=True)
    supplier_id = fields.Many2one('res.partner', string='Preferred Supplier', required=True)

    @api.constrains('product_id', 'supplier_id')
    def _check_unique_reorder_rule(self):
        for rule in self:
            existing_rule = self.search([
                ('product_id', '=', rule.product_id.id),
                ('id', '!=', rule.id)
            ])
            if existing_rule:
                raise ValidationError("A reorder rule for this product already exists.")

    def _generate_replenishment_order(self, rule):
        """This method creates the automated order based on the applicable reordering rule.
        Created purchase order will be in draft state so the corresponding user can check and confirm it.
        Params:
            self: Object/Recordset of the class CustomProductReorderRule
        Return:
            None
        """
        purchase_order = self.env['purchase.order'].create({
            'partner_id': rule.supplier_id.id,
            'is_approval_required': True,
            'order_line': [(0, 0, {
                'product_id': rule.product_id.id,
                'product_qty': rule.reorder_qty,
                'price_unit': rule.product_id.standard_price,
                'date_planned': fields.Date.today() + timedelta(days=rule.lead_time),
            })]
        })
        group = self.env.ref('auto_reorder.group_auto_reorder_approval')
        template = self.env.ref('auto_reorder.email_template_auto_reorder_approval')
        template.email_from = self.env.company.email
        template.email_to = self.env.user.partner_id.email
        template.body_html = """<p>Hello %s,</p>
                    <p>There is a replenishment PO (%s) created for the product %s waiting for your approval.</p>
                    <p>Regards,<br/>Your Company</p>""" %(self.env.user.name, purchase_order.name, rule.product_id.product_tmpl_id.name)
        if group and template:
            for user in group.users:
                template.send_mail(user.id, force_send=True)

    def _check_stock_levels(self):
        """This method checks the stock levels for triggering the order based on the applicable reordering rule.
            Params:
                self: Object/Recordset of the class CustomProductReorderRule"""
        rules = self.search([])
        for rule in rules:
            product = rule.product_id
            stock_qty = product.qty_available
            if stock_qty < rule.min_qty:
                self._generate_replenishment_order(rule)
