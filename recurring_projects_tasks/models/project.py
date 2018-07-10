# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_template = fields.Boolean(
        string="Template",
        default=False,
        copy=False
    )
    b_duplicate = fields.Boolean(
        string="Recurring",
        copy=False,
        default=False
    )
    date_duplicate = fields.Date(
        string="Date Recurring",
        copy=False,
        default=fields.Date.context_today
    )
    rate_duplicate = fields.Selection([
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year')
        ], string="Rate Recurring",
        default='month', copy=False
    )
    rate_interval = fields.Integer(
        string="Rate interval",
        default=1,
        copy=False
    )
    date_end = fields.Date(
        string="Date end Recurring",
        copy=False,
    )
    count_duplicates = fields.Integer(
        string="Count Duplicates",
        default=0,
        copy=False,
        readonly=True
    )
    project_template_id = fields.Many2one(
        'project.project',
        string="Project template original",
        copy=False
    )
    duplicate_projects_ids = fields.One2many(
        'project.project',
        'project_template_id',
        string="Projects duplicates",
    )

    type_project_ids = fields.Many2many(
        'project.task.type', 'project_type_type_rel',
        'project_id', 'type_id', string='Tasks Stages')

    """
    Add sequences properly and change duplicated depending tasks
    """
    @api.multi
    def copy(self, default=None):
        if default:
            if self.project_template:
                default['project_template_id'] = self.id
        else:
            if self.project_template:
                default = {
                    'project_template_id': self.id
                }
        res = super(ProjectProject, self).copy(default)
        for task in self.env['project.task'].search([
            ('project_id', '=', res.id),
            ('dependency_task_ids', '!=', False),
           ]):
            ids_task_depends = []
            for task_depen in task.dependency_task_ids:
                ids_task_depends.append(self.env['project.task'].search([
                    ('name', '=', task_depen.name),
                    ('project_id', '=', task.project_id.id)
                    ], limit=1).id)
            task.dependency_task_ids = [(6, 0, ids_task_depends)]
        return res

    """
    Check which projects must duplicate
    """
    @api.model
    def auto_duplicate_project(self):
        max_date = date.today() + relativedelta(months=2)
        for project in self.env['project.project'].search([
            ('b_duplicate', '!=', False),
            ('date_duplicate', '!=', False),
            ('date_duplicate', '<=', date.today()),
           ]):
            fecha_calculada = fields.Date.from_string(
                                project.date_duplicate)
            if project.rate_duplicate == 'day':
                fecha_calculada = fecha_calculada + relativedelta(
                    days=project.rate_interval*project.count_duplicates
                    )
            elif project.rate_duplicate == 'month':
                fecha_calculada = fecha_calculada + relativedelta(
                    months=project.rate_interval*project.count_duplicates
                    )
            elif project.rate_duplicate == 'year':
                fecha_calculada = fecha_calculada + relativedelta(
                    years=project.rate_interval*project.count_duplicates
                    )
            datendpro =\
                fields.Date.from_string(project.date_end) or max_date
            while fecha_calculada <= datendpro:
                project = project.with_context(
                    rate_cron=project.rate_interval*project.count_duplicates,
                    type_rate_cron=project.rate_duplicate
                )
                new_project = project.copy()
                name_split = '(copy)'
                if '(copia)' in new_project.name:
                    name_split = '(copia)'
                new_project.write({
                    'name': new_project.name.split(name_split)[0] +
                    str(fecha_calculada),
                    'b_duplicate': False,
                    'date_duplicate': False,
                    'rate_duplicate': False,
                    'count_duplicates': False,
                    'rate_interval': 1,
                    'date_end': False,
                    })
                project.count_duplicates += 1
                fecha_calculada = fields.Date.from_string(
                                project.date_duplicate)
                if project.rate_duplicate == 'day':
                    fecha_calculada = fecha_calculada + relativedelta(
                        days=project.rate_interval*project.count_duplicates
                        )
                elif project.rate_duplicate == 'month':
                    fecha_calculada = fecha_calculada + relativedelta(
                        months=project.rate_interval*project.count_duplicates
                        )
                elif project.rate_duplicate == 'year':
                    fecha_calculada = fecha_calculada + relativedelta(
                        years=project.rate_interval*project.count_duplicates
                        )
            if project.date_end and fecha_calculada >= datendpro:
                project.write({
                        'b_duplicate': False,
                        'date_duplicate': False,
                        'rate_duplicate': False,
                        'count_duplicates': False,
                        'rate_interval': 1,
                        'date_end': False,
                        })
