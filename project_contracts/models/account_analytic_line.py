# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    contract_id = fields.Many2one(
        'project.contract',
        related='account_id.project_ids.contract_id',
        store=True,
        string=_('Contract')
    )
    contract_hours = fields.Boolean(
        related='product_id.categ_id.contract_hours',
        store=True,
        string=_('Category Hours')
    )

    @api.multi
    @api.constrains('account_id')
    def _check_contract(self):
        for sel in self:
            if sel.contract_id and not sel.move_id and \
               sel.contract_id.state != 'open':
                raise ValidationError(_(
                    "Can't create the line, please renew the contract."))