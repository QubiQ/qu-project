# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ <marsal.isern@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    sale_id = fields.One2many(
        'sale.order',
        related='analytic_account_id.sale_ids',
        string='Sale Order')

