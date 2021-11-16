# Copyright 2018 Valentín Vinagre <valentin.vinagre@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    show_hours_report = fields.Boolean(
        default=True,
        string=_('Show on Hours Consumption Report')
    )
