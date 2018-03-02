# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ <marsal.isern@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    code = fields.Char(
        string='Project Number', required=True, default="/", readonly=True)

    _sql_constraints = [
        ('project_unique_code', 'UNIQUE (code)',
         _('The code must be unique!')),
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', '/') == '/':
            vals['code'] = self.env['ir.sequence'].next_by_code('project.code')
        return super(ProjectProject, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['code'] = self.env['ir.sequence'].next_by_code('project.code')
        return super(ProjectProject, self).copy(default)
