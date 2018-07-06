# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'
    _order = "priority desc, sequence, name, id"

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Priority'),
        ('2', 'Urgent'),
        ('3', 'Urgent-Priority')
    ], default='0', string="Priority")
