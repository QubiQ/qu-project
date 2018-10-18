# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    create_opportunity = fields.Boolean(
        default=False,
        string=_('Create opportunity')
    )
    stage_id = fields.Many2one(
        comodel_name='crm.stage',
        string=_('Stage')
    )
