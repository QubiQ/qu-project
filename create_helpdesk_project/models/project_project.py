# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, exceptions, api, _


class ProjectProject(models.Model):
    _inherit = "project.project"

    helpdesk_ids = fields.One2many(
        comodel_name='helpdesk.team',
        inverse_name='project_id'
    )

    def create_helpdesk_team(self):
        if self.helpdesk_ids:
            raise exceptions.Warning(
                _("There is already a helpdesk for the project, the name of the helpdesk is %s!" % ', '.join(self.helpdesk_ids.mapped('name')))
            )
        return {
            'name': _('Create helpdesk'),
            'type': 'ir.actions.act_window',
            'res_model': 'create.helpdesk.wizard',
            'res_id': self.env['create.helpdesk.wizard'].create({
                'name': self.name,
                'email_alias': self.alias_name,
                'allow_timesheet': self.allow_timesheets
            }).id,
            'view_id': self.env.ref('create_helpdesk_project.create_helpdesk_wizard').id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'
            }
