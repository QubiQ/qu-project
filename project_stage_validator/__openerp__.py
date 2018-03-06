# -*- coding: utf-8 -*-
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project Stage Validators",
    "summary": "Project Stage Validators",
    "version": "10.0.1.0.0",
    "category": "Project",
    "website": "https://www.qubiq.es",
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
        "project",
        "project_issue",
    ],
    "data": [
        "views/project_project.xml",
        "views/project_task_type.xml",
    ],
}
