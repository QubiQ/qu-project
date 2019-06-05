# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_analytic_ids = fields.Many2many(
        'account.analytic.account',
        compute='_get_account_analytic_ids',
        string=_("Account analytic"),
        store=True
    )

    @api.multi
    @api.depends('invoice_line_ids.account_analytic_id')
    def _get_account_analytic_ids(self):
        for sel in self:
            account_analytic_ids = set()
            account_analytic_ids.update(
                sel.invoice_line_ids.mapped('account_analytic_id').ids
            )
            sel.account_analytic_ids =\
                self.env['account.analytic.account'].browse(
                    list(account_analytic_ids)
                )
