# -*- coding: utf-8 -*-
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProjectProject(models.Model):
    _inherit = "project.project"

    validators_ids = fields.Many2many(
        'res.users',
        'project_users_validators_rel',
        string="Validators")
