# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    contract_id = fields.Many2one(
        'project.contract',
        string=_('Contract'),
        copy=False,
    )

    type_project = fields.Selection(
        string=_('Type of Project'),
        required=True,
        default='billable',
        selection=[('billable', _('Billable')), ('no_billable', _('No Billable'))]
    )
