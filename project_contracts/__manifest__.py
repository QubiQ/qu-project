# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

{
    'name': 'Project Contracts',
    'summary': 'Contracts for projects',
    'version': '11.0.1.0.0',
    'author': 'QubiQ, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.qubiq.es',
    'depends': [
        'base',
        'project',
        'account',
        'product',
        'hr_timesheet',
    ],
    'data': [
        'data/email_template.xml',
        'data/cron.xml',
        'data/sequence.xml',
        'views/project_contract.xml',
        'views/project.xml',
        'views/product_category.xml',
        'views/project_task.xml',
        'security/ir.model.access.csv',
    ],
    'category': 'Project',
    'installable': True,
    'application': False,
}
