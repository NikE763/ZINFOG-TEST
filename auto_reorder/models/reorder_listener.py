# -*- coding: utf-8 -*-
from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        move = super(StockMove, self).create(vals)
        if move.state == 'done':
            move.product_id._check_reorder_rules()
        return move


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _check_reorder_rules(self):
        ReorderRule = self.env['custom.product.reorder.rule']
        for product in self:
            rule = ReorderRule.search([('product_id', '=', product.id)], limit=1)
            if rule and product.qty_available <= rule.min_qty:
                ReorderRule._create_replenishment_orders([(product, rule)])
