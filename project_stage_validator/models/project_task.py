# -*- coding: utf-8 -*-
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.multi
    def write(self, vals):
        res = super(ProjectTask, self).write(vals)

        for task in self:
            if task.stage_id.needs_validator:
                user_obj = task.env['res.users'].browse(
                    task.env.context.get('uid'))
                if user_obj not in task.project_id.validators_ids:
                    raise ValidationError(_(
                        'It was not possible to change the stage '
                        'of the task.\n\n '
                        'The stage needs a validation before changing.'))

        return res
