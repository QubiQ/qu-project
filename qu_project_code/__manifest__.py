# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ <marsal.isern@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Code",
    "version": "10.0.1.0.0",
    "category": "Project Management",
    "author": "QubiQ, "
              "Odoo Community Association (OCA)",
    "website": "http://www.qubiq.es",
    "license": "AGPL-3",
    "contributors": [
        "Marçal Isern <marsal.isern@qubiq.es>",
    ],
    "depends": [
        "project",
    ],
    "data": [
        "data/project_sequence.xml",
        "views/project_view.xml",
    ],
    'installable': True,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}
