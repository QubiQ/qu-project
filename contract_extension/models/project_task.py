# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def write(self, vals):
        project_id = self.project_id
        remaining = project_id.hours_available - project_id.hours_worked
        # If the diference is exactly 0.00 the sale order won't appear
        # on the menu 'Sale orders to renew'
        if remaining <= -0.10:
            raise ValidationError(_(
                'You can\'t add another timesheet line to this project '
                'because the contract associated has run out of hours.\n\n '
                'Current difference: %s Hour(s)') % (format(remaining, '.2f')))

        result = super(ProjectTask, self).write(vals)
        return result
