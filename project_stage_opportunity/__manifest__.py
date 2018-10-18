# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Project Stage Opportunity",
    "summary": "Create an opportunity when a task stage is changed",
    "version": "10.0.1.0.0",
    "category": "Project",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "project",
        "crm"
    ],
    "data": [
        "views/project_task_type.xml"
    ],
}
