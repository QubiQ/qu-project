# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Modify Followers Issue",
    "summary": "Modify list of followers from a helpdesk ticket",
    "version": "11.0.1.0.0",
    "category": "Helpdesk",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'helpdesk'
    ],
    "data": [
        'wizard/modify_followers_issue_wizard.xml',
        'views/helpdesk_ticket_view.xml',
    ],
}
