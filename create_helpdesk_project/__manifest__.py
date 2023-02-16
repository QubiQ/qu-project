# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Create Helpdesk Project",
    "summary": "Create a helpdesk from a project",
    "version": "16.0.1.0.0",
    "category": "project",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        'project',
        'helpdesk',
    ],
    "data": [
        'views/project_project_view.xml',
        'views/helpdesk_stages_view.xml',
        'wizard/create_helpdesk_wizard.xml',
    ],
}
