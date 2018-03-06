# -*- coding: utf-8 -*-
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from odoo.exceptions import ValidationError


class ProjectIssue(models.Model):
    _inherit = "project.issue"

    @api.multi
    def write(self, vals):
        res = super(ProjectIssue, self).write(vals)

        for issue in self:
            if issue.stage_id.needs_validator:
                user_obj = issue.env['res.users'].browse(
                    issue.env.context.get('uid'))
                if user_obj not in issue.project_id.validators_ids:
                    raise ValidationError(_(
                        'It was not possible to change the stage '
                        'of the issue.\n\n '
                        'The stage needs a validation before changing.'))

        return res
