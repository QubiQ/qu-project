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
    billable = fields.Boolean(
        string=_('Billable'),
        default=lambda self: self._check_billable()
    )

    @api.model
    def _check_billable(self):
        is_billable = True
        if self._context.get('default_project_id', None):
            is_billable = 'billable' == self.env['project.project'].browse(
                self._context['default_project_id']).type_project
        elif self._context.get('invoice', None):
            if self._context['invoice'][0]\
                    .account_analytic_ids[0].project_ids:
                is_billable = 'billable' == self.env['account.move'].browse(
                    self._context['invoice'][0].id)\
                    .account_analytic_ids[0].project_ids[0].type_project
        return is_billable

    @api.constrains('account_id')
    def _check_contract(self):
        for sel in self:
            if sel.contract_id and not sel.move_id and \
               sel.contract_id.state != 'open':
                raise ValidationError(_(
                    "Can't create the line, please renew the contract."))
