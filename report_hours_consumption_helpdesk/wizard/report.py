# Copyright 2018 Xavier Piernas <xavier.piernas@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ReportHoursConsumption(models.TransientModel):
    _inherit = 'report.hours.consumption'

    def get_type(self, aal):
        res = super(ReportHoursConsumption, self).get_type(aal)
        if res in ['Manual', 'Tarea'] and aal.helpdesk_ticket_id:
            res = 'Helpdesk'
        return res

    def get_creation_date(self, aal, kind):
        res = super(ReportHoursConsumption, self).get_creation_date(aal, kind)
        if kind == 'Helpdesk':
            res = aal.helpdesk_ticket_id.create_date or ''
        return res

    def get_contact(self, aal, kind):
        res = super(ReportHoursConsumption, self).get_contact(aal, kind)
        if kind == 'Helpdesk':
            res = aal.helpdesk_ticket_id.partner_id or ''
        return res

    def get_origin(self, aal, kind):
        res = super(ReportHoursConsumption, self).get_origin(aal, kind)
        if kind == 'Helpdesk':
            res = aal.helpdesk_ticket_id.name or ''
        return res

    def get_state(self, aal, kind):
        res = super(ReportHoursConsumption, self).get_state(aal, kind)
        if kind == 'Helpdesk':
            res = aal.helpdesk_ticket_id.stage_id.name or ''
        return res
