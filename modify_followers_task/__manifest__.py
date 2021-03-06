# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Modify Followers Task",
    "summary": "Modify list of followers from a project task",
    "version": "12.0.1.0.0",
    "category": "Project",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        'project'
    ],
    "data": [
        'wizard/modify_followers_task_wizard.xml',
        'views/project_task_view.xml',
    ],
}
