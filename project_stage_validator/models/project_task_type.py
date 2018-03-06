# -*- coding: utf-8 -*-
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    needs_validator = fields.Boolean(string="Needs validator", default=False)
