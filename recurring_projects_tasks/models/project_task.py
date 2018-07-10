# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_template = fields.Boolean(
        string="Task Template",
        related="project_id.project_template",
        store=True,
        readonly=True
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
        ],
        string="Rate duplicate",
        default='month',
        copy=False
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
    task_template_id = fields.Many2one(
        'project.task',
        string="Task template original",
        copy=False
    )
    duplicate_tasks_ids = fields.One2many(
        'project.task',
        'task_template_id',
        string="Tasks duplicates",
        copy=False
    )
    dependency_task_ids = fields.Many2many(
        string='Dependencies',
        comodel_name='project.task',
        relation='project_task_dependency_task_rel',
        column1='task_id', column2='dependency_task_id'
    )
    date_deadline = fields.Date(
        copy=True
    )

    @api.multi
    def copy(self, default=None):
        res = super(ProjectTask, self).copy(default)
        if 'rate_cron' in self._context and res.date_deadline:
            type_rate = self._context['type_rate_cron']
            rate = self._context['rate_cron']
            if type_rate == 'day':
                fecha_calculada = fields.Date.from_string(res.date_deadline) +\
                    relativedelta(days=rate)
            elif type_rate == 'month':
                fecha_calculada = fields.Date.from_string(res.date_deadline) +\
                    relativedelta(months=rate)
            elif type_rate == 'year':
                fecha_calculada = fields.Date.from_string(res.date_deadline) +\
                    relativedelta(years=rate)
            res.date_deadline = fecha_calculada
        else:
            res.date_deadline = None
        return res

    """
    Check which projects must duplicate
    """
    @api.model
    def auto_duplicate_task(self):
        max_date = date.today() + relativedelta(months=2)
        for task in self.env['project.task'].search([
            ('b_duplicate', '!=', False),
            ('date_duplicate', '!=', False),
            ('date_duplicate', '<=', date.today()),
           ]):
            fecha_calculada = fields.Date.from_string(
                                task.date_duplicate)
            deadline = fields.Date.from_string(
                                task.date_deadline)
            intervalo = fields.Date()
            fecha_sumar = fields.Date()
            if task.rate_duplicate == 'day':
                fecha_calculada = fecha_calculada + relativedelta(
                    days=task.rate_interval*task.count_duplicates
                    )
                intervalo = relativedelta(days=task.rate_interval)
            elif task.rate_duplicate == 'month':
                fecha_calculada = fecha_calculada + relativedelta(
                    months=task.rate_interval*task.count_duplicates
                    )
                intervalo = relativedelta(months=task.rate_interval)
            elif task.rate_duplicate == 'year':
                fecha_calculada = fecha_calculada + relativedelta(
                    years=task.rate_interval*task.count_duplicates
                    )
                intervalo = relativedelta(years=task.rate_interval)
            datendtas =\
                fields.Date.from_string(task.date_end) or max_date
            fecha_sumar = intervalo
            while fecha_calculada <= datendtas:
                new_task = task.copy()
                name_split = '(copy)'
                if '(copia)' in new_task.name:
                    name_split = '(copia)'
                new_task.write({
                    'name': new_task.name.split(name_split)[0] +
                    str(fecha_calculada),
                    'b_duplicate': False,
                    'date_duplicate': False,
                    'rate_duplicate': False,
                    'count_duplicates': False,
                    'rate_interval': 1,
                    'date_end': False,
                    'task_template_id': task.id,
                    'date_deadline': deadline + fecha_sumar
                    })
                fecha_sumar += intervalo
                task.count_duplicates += 1
                fecha_calculada = fields.Date.from_string(
                                task.date_duplicate)
                if task.rate_duplicate == 'day':
                    fecha_calculada = fecha_calculada + relativedelta(
                        days=task.rate_interval*task.count_duplicates
                        )
                elif task.rate_duplicate == 'month':
                    fecha_calculada = fecha_calculada + relativedelta(
                        months=task.rate_interval*task.count_duplicates
                        )
                elif task.rate_duplicate == 'year':
                    fecha_calculada = fecha_calculada + relativedelta(
                        years=task.rate_interval*task.count_duplicates
                        )
            if task.date_end and fecha_calculada >= datendtas:
                task.write({
                        'b_duplicate': False,
                        'date_duplicate': False,
                        'rate_duplicate': False,
                        'count_duplicates': False,
                        'rate_interval': 1,
                        'date_end': False,
                        }
                    )
