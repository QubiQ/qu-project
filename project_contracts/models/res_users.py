# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    project_contracts_ids = fields.One2many(
        comodel_name='project.contract',
        inverse_name='manager_id',
        string=_('Project Contracts'),
        copy=False
    )
