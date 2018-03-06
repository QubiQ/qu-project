# -*- coding: utf-8 -*-
# Copyright (c) 2017 QubiQ (http://www.qubiq.es)
#                    Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Contract Extension",
    "summary": "Add functionalities to Contract module",
    "version": "10.0.1.0.0",
    "category": "Contract",
    "website": "https://www.qubiq.es/",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "sale",
        "account",
        "contract",
        "project",
        "hr_timesheet",
    ],
    "data": [
        'views/project_view.xml',
    ],
}
