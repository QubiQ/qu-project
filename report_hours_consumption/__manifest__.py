# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

{
    'name': 'Report Project Hours Consumption',
    'version': '11.0.0.1.0',
    'sequence': 14,
    'summary': 'Project, report, account',
    'description': """
        New report for hours consumption from projects.
        Dependencias de python: xlsxwriter, openpyxl
    """,
    'author': 'QubiQ SL',
    'website': 'https://www.qubiq.es',
    'external_dependencies': {
        'python': [
            'xlwt',
            'openpyxl'
        ]
    },
    'depends': [
        'project_contracts',
        'file_download',
    ],
    'category': 'report',
    'data': [
        'wizard/report.xml',
    ],
    'installable': True,
    'application': False,
}
