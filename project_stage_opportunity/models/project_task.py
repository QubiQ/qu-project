# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _check_opportunity(self):
        return self.env['crm.lead'].search_count([
            ('name', '=', 'OP-<' + self.project_id.name + '>'),
            ('partner_id', '=', self.partner_id.id),
            ('project_id', '=', self.project_id.id)
        ])

    def _prepare_opportunity_data(self):
        return {
            'name': 'OP-<' + self.project_id.name + '>',
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'project_id': self.project_id.id,
            'type': 'opportunity',
            'stage_id': self.stage_id.stage_id.id
        }

    @api.multi
    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if self.stage_id.create_opportunity and self._check_opportunity() == 0:
            self.env['crm.lead'].create(
                self._prepare_opportunity_data()
            )._onchange_partner_id()
        return res
