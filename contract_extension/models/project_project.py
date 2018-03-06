# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    hours_worked = fields.Float(
        compute='_calculate_hours_worked',
        string='Total worked time',
    )
    hours_available = fields.Float(
        compute='_calculate_hours_available',
        string='Total hours available',
    )

    @api.multi
    def _calculate_hours_worked(self):
        project_obj = self.env['project.project']
        dp = 2
        self_ids = []
        for project in self:
            self_ids.append(project.id)
        self_ids = tuple(self_ids)

        if self_ids:
            self._cr.execute(
                '''
                    SELECT
                        account_analytic_line.project_id,
                        COALESCE(SUM(unit_amount), 0.0) AS hours_qty
                    FROM
                        account_analytic_line
                    WHERE
                        account_analytic_line.project_id IN %s
                    GROUP BY
                        account_analytic_line.project_id
                ''', (self_ids,)
            )
            for row in self._cr.dictfetchall():
                acc = project_obj.browse(row['project_id'])
                if acc:
                    acc.hours_worked = round(row['hours_qty'], dp)

    @api.multi
    def _calculate_hours_available(self):
        dp = 2

        for project in self:
            hours_available = 0
            analytic_lines = self.env['account.analytic.line'].search([
                ('account_id', '=', project.analytic_account_id.id),
                ('project_id', '=', None),
                ('product_id', 'not in', (12, 14))])
            for line in analytic_lines:
                hours_available += line.unit_amount

            project.hours_available = round(hours_available, dp)
