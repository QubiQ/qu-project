# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    contract_count = fields.Integer(
        string=_('Number Contracts'),
        compute='_get_contract_count'
    )
    project_contract_ids = fields.One2many(
        string=_('Contracts'),
        comodel_name='project.contract',
        inverse_name='partner_id'
    )

    def _get_contract_count(self):
        for sel in self:
            contract_count = 0
            if sel.project_contract_ids:
                contract_count = len(self.env['project.contract'].search([
                    ('partner_id', '=', sel.id)
                ]))
            sel.contract_count = contract_count

    def link_contract(self):
        tree_view = self.env.ref(
            'project_contracts.view_tree_project_contract')
        form_view = self.env.ref(
            'project_contracts.view_form_project_contract')
        return {
            'name': _('Contract'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.contract',
            'view_id': tree_view.id,
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('partner_id', '=', self.id)]
        }
