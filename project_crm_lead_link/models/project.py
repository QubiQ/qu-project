# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ <marsal.isern@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    lead_id = fields.One2many(
        'crm.lead','project_id',string='Lead/Oportunity ')

