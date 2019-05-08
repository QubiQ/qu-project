# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    project_id = fields.Many2one(
        comodel_name='project.project',
    )
