# Copyright 2018 Valentín Vinagre <valentin.vinagre@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Report Hours Consumption",
    "summary": "Get an Excel report about project hours consumption",
    "version": "13.0.1.0.0",
    "category": "Project",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [
            "xlwt",
            "openpyxl"
        ]
    },
    "depends": [
        "project_contracts",
        "file_download",
    ],
    "data": [
        "wizard/report.xml",
        "views/product_category.xml"
    ],
}
