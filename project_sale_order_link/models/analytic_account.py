# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ <marsal.isern@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    sale_ids = fields.One2many(
        'sale.order','related_project_id',string='Sale Order')

