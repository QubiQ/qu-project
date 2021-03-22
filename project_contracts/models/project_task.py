# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, api, _
import logging


class ProjectTask(models.Model):
    _inherit = 'project.task'

    beyond_scope = fields.Boolean(
        string=_('Beyond Scope'),
        default=False
    )

    billable_hours = fields.Float(compute='_compute_project_billable_worked_hours',
        readonly=True, string='Billable hours')

    no_billable_hours = fields.Float(compute='_compute_project_billable_worked_hours',
        readonly=True, string='No billable hours')

    billable_child_hours = fields.Float(compute='_compute_project_billable_worked_hours',
        readonly=True, string='SubTask Billable Hours')

    no_billable_child_hours = fields.Float(compute='_compute_project_billable_worked_hours',
        readonly=True, string='SubTask No Billable Hours')

    remaining_billable_hours = fields.Float(compute='_compute_project_billable_worked_hours',
        readonly=True, string='Remaining Billable Hours')

    total_billable_hours_spent = fields.Float(compute='_compute_project_billable_worked_hours',
        readonly=True, string='Total Billable Hours')

    type_project = fields.Selection(related='project_id.type_project')

    def _compute_project_billable_worked_hours(self):
        for sel in self:
            sel.billable_hours = 0
            sel.no_billable_hours = 0
            sel.billable_child_hours = 0
            sel.no_billable_child_hours = 0
            for line in sel.timesheet_ids:
                if line.billable:
                    sel.billable_hours += line.unit_amount
                else:
                    sel.no_billable_hours += line.unit_amount
            if len(sel.child_ids) != 0:
                for child_task in sel.child_ids:
                    for child_line in child_task.timesheet_ids:
                        if child_line.billable:
                            sel.billable_child_hours += child_line.unit_amount
                        else:
                            sel.no_billable_child_hours += child_line.unit_amount

            sel.total_billable_hours_spent = sel.billable_child_hours + sel.billable_hours
            sel.remaining_billable_hours = sel.planned_hours - sel.total_billable_hours_spent


