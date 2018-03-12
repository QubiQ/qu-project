# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
{
    'name': 'Views Projects',
    'version': '10.0.1.0.0',
    'author': 'QubiQ, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.qubiq.es',
    'depends': [
                'base',
                'project',
                'project_task_default_stage',
                'project_task_add_very_high',
                'project_department',
                'project_timeline',
                'web_timeline',
                ],
    'data': [
        'views/project.xml',
    ],
    'category': 'Projects',
    'demo': [],
    'installable': True,
    'application': False,
}
