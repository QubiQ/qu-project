# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class CreateTicketWizard(models.TransientModel):
    _name = "create.helpdesk.wizard"

    name = fields.Char(
        string=_('Name'),
        required=True
    )
    email_alias = fields.Char(
        string=_('Email Alias')
    )
    allow_timesheet = fields.Boolean(
        string=_('Allow timesheets'),
        default=True,
    )
    helpdesk_stage_ids = fields.Many2many(
        comodel_name='helpdesk.stage',
        string=_('Helpdesk Stages'),
        default=lambda self: [(6, 0, self.env['helpdesk.stage'].search([
            ('is_stages_project', '=', True)
        ]).ids)]
    )

    @api.multi
    def create_helpdesk(self):
        helpdesk_team = self.env['helpdesk.team'].create({
            'name': self.name,
            'use_helpdesk_timesheet': self.allow_timesheet,
            'project_id': self._context.get('active_id'),
            'alias_name': self.email_alias,
            'company_id': self.env['project.project'].browse(
                self._context.get('active_id')
            ).company_id.id,
            'stage_ids': [(6, 0, self.helpdesk_stage_ids.ids)]
        })
        action = self.env.ref('create_helpdesk_project.helpdesk_team_action_form').read()[0]
        action['res_id'] = helpdesk_team.id
        return action
