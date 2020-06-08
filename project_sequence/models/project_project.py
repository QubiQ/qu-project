# Copyright 2020 Jesus Ramoneda <jesus.ramoneda@qubiq.es>
# License AGPL-3.0 or later (https: //www.gnu.org/licenses/agpl).
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def get_project_sequence(self):
        return self.env['ir.sequence'].next_by_code(
           'project.project') or ''

    name = fields.Char(default=get_project_sequence)
