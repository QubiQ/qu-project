# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError




class ProjectProject(models.Model):
    _inherit = 'project.project'

    priority = fields.Selection([
            ('0', 'Normal'),
            ('1', 'High'),
            ('2', 'Very High')
        ], default='0', index=True
    )

