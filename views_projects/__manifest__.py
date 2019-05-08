# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

{
    'name': 'Views Projects',
    'version': '12.0.1.0.0',
    'author': 'QubiQ, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.qubiq.es',
    'depends': [
                'base',
                'project',
                'project_task_default_stage',
                'project_task_add_very_high',
                'project_timeline',
                'web_timeline',
                ],
    'data': [
        'views/project.xml',
    ],
    'category': 'Project',
    'installable': True,
    'application': False,
}
