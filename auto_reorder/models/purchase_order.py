# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseApproval(models.Model):
    _inherit = 'purchase.order'

    is_approval_required = fields.Boolean('Approval Required')

    def approve_po(self):
        """Approve the replenishment PO"""
        for rec in self.filtered(lambda l: l.is_approval_required and l.state!='purchase'):
            rec.button_confirm()
