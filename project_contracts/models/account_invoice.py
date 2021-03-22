# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    account_analytic_ids = fields.Many2many(
        'account.analytic.account',
        compute='_get_account_analytic_ids',
        string=_("Account analytic"),
        store=True
    )

    @api.depends('invoice_line_ids.analytic_account_id')
    def _get_account_analytic_ids(self):
        for sel in self:
            sel.account_analytic_ids = sel.invoice_line_ids.\
                mapped('analytic_account_id')
