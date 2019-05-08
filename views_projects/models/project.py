# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    priority = fields.Selection([
            ('0', 'Normal'),
            ('1', 'High'),
            ('2', 'Very High')
        ], default='0', index=True
    )
    date_start = fields.Datetime(
        string="Date start",
        default=fields.Datetime.now()
    )
    date_end_project_date = fields.Date(
        string="Date end format date",
        compute="get_date_end_project_date",
        copy=False,
        store=True
    )

    @api.depends('date')
    @api.multi
    def get_date_end_project_date(self):
        for sel in self:
            if sel.date:
                sel.date_end_project_date =\
                    fields.Datetime.from_string(
                                sel.date).date()
