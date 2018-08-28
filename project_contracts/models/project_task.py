# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    beyond_scope = fields.Boolean(
        string=_('Beyond Scope'),
        default=False
    )
