# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    contract_hours = fields.Boolean(
        string=_('Contract Hours'),
        default=False,
        helps=_('Category of product for the maximum hours to contracts.')
    )
