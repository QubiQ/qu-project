# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ SL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Recurring Projects and Tasks',
    'version': '10.0.1.0.0',
    'sequence': 14,
    'summary': 'Projects',
    'description': "Create recurring projects and tasks",
    'author': 'QubiQ SL',
    'website': 'https://www.qubiq.es',
    'depends': [
                'base',
                'project',
                'hr_timesheet',
                'project_task_default_stage',
                ],
    'data': [
        'data/ir_cron.xml',
        'views/project.xml',
        'views/project_task.xml',
    ],
    'category': 'Project',
    'installable': True,
}
