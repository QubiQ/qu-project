# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Report Hours Consumption Helpdesk",
    "summary": "Extends Report Hours Consumption module with Helpdesk",
    "version": "13.0.1.0.0",
    "category": "Project",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        'report_hours_consumption',
        'account',
        'helpdesk_timesheet',
        'helpdesk',
        'project_contracts',
    ],
    "data": [
        'views/helpdesk_ticket_view.xml'
    ],
}
