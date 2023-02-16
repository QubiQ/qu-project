# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Contract Price Hour',
    'summary': 'Price for hour in a contract',
    'version': '13.0.1.0.0',
    'author': 'QubiQ, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.qubiq.es',
    'depends': [
        'project_contracts',
        'account',
    ],
    'data': [
        'views/project_contract_view.xml',
    ],
    'category': 'Project',
    'installable': False,
    'application': False,
}
