# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)

from openerp import models, api, fields
from datetime import datetime


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_timer_started = fields.Boolean('Task started', default=False)
    task_timer_start = fields.Datetime('Task work started at')
    task_timer_finish = fields.Datetime('Task work finished at')

    @api.multi
    def start_task_timer(self):
        for task in self:
            task.task_timer_started = True
            task.task_timer_start = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")

    @api.multi
    def stop_task_timer(self):
        for task in self:
            task.task_timer_started = False
            task.task_timer_finish = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
            dstart = datetime.strptime(
                task.task_timer_start, '%Y-%m-%d %H:%M:%S')
            dfinish = datetime.strptime(
                task.task_timer_finish, '%Y-%m-%d %H:%M:%S')
            time_of_work = (dfinish - dstart).seconds / 3600.0
            task.update({
                        'work_ids': [(0, 0, {
                            'name': 'Trabajo en tarea',
                            'hours': time_of_work,
                            'date': datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"),
                            'user_id': task._uid,
                            })],
                        })
