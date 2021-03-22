# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class HelpdeskStages(models.Model):
    _inherit = "helpdesk.stage"

    is_stages_project = fields.Boolean(
        string=_('Stage from project'),
    )
