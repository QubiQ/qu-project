# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ProjectContract(models.Model):
    _inherit = 'project.contract'

    hour_price = fields.Float(
        string=_('Hour Price'),
        compute='_get_hours_price',
    )

    @api.multi
    def _get_hours_price(self):
        for sel in self:
            invoice_ids = self.env['account.invoice'].sudo().search([
                    ('account_analytic_ids', 'in',
                        sel.project_ids.mapped('analytic_account_id').ids),
                    ('partner_id', '=', sel.partner_id.id),
                    ('state', 'in', ('open', 'paid')),
                    ('type', '=', 'out_invoice')
                ])
            quantity = 0.0
            subtotal = 0.0
            for invoice in invoice_ids:
                # logging.info(invoice.partner_id.name)
                if quantity == 0.0 or subtotal == 0.0:
                    for line in invoice.invoice_line_ids.filtered(
                       lambda x: x.product_id.categ_id.contract_hours):
                        subtotal += line.price_subtotal
                        quantity += line.quantity
                else:
                    break
            sel.hour_price = 0.0 if quantity == 0.0 else subtotal/quantity
