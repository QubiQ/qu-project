# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)


from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectContract(models.Model):
    _name = 'project.contract'
    _description = "Project Contracts"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string=_('Contract Name'),
        required=True,
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string=_('Customer'),
        domain="[('customer', '=', True), ('parent_id', '=', False)]",
        required=True,
        copy=False,
    )
    project_ids = fields.One2many(
        comodel_name='project.project',
        inverse_name='contract_id',
        string=_('Projects'),
        copy=False
    )
    manager_id = fields.Many2one(
        'res.users',
        string=_('Manager'),
        default=lambda self: self.env.user.id,
        track_visibility='onchange'
    )
    reference = fields.Char(
        string=_("Reference"),
        copy=False,
        readonly=True,
    )
    date_start = fields.Date(
        string=_('Date Start'),
        default=fields.Date.context_today
    )
    date_end = fields.Date(
        string=_('Date End')
    )
    quantity_max = fields.Float(
        string=_('Unit prepayment'),
        compute_sudo=True,
        compute='_get_quantity_max',
        help=_('Maximum time to work on the project.')
    )
    hours_quantity = fields.Float(
        string=_('Hours consumed'),  # traducir
        compute_sudo=True,
        compute='_get_hours_quantity'
    )
    remaining_hours = fields.Float(
        string=_('Hours left'),  # traducir
        compute='_get_remaining_hours',
        compute_sudo=True,
        help=_('Quantity_max - Hours_quantity'),
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id,
        string=_('Company')
    )
    attachment_ids = fields.One2many(
        'ir.attachment',
        compute='_compute_attachment_ids',
        string=_('Main Attachments'),
        help=_("Attachment that don't come from message.")
    )
    state = fields.Selection([
        ('open', _('In Progress')),
        ('pending', _('To renew')),
        ('close', _('Closed')),
        ('cancelled', _('Cancelled'))
        ], string='Status', required=True,
        default='open',
        track_visibility='onchange', copy=False
    )
    invoice_count = fields.Integer(
        string=_('Number Invoices'),
        compute='_get_invoice_count'
    )

    @api.multi
    def unlink(self):
        for order in self:
            if order.state != 'cancelled':
                raise UserError(_('You can not delete a contract!'
                                  ' Try to cancel it before.'))
        return super(ProjectContract, self).unlink()

    @api.multi
    def _get_invoice_count(self):
        for sel in self:
            invoice_count = 0
            if sel.project_ids:
                invoice_count = len(self.env['account.invoice'].search([
                    ('account_analytic_ids', 'in',
                        sel.project_ids.mapped('analytic_account_id').ids),
                    ('partner_id', '=', sel.partner_id.id),
                    ('company_id', '=', sel.company_id.id)
                ]))
            sel.invoice_count = invoice_count

    @api.multi
    def invoice_projects(self):
        invoice_ids = []
        for sel in self:
            invoice_ids = self.env['account.invoice'].search([
                ('account_analytic_ids', 'in',
                    sel.project_ids.mapped('analytic_account_id').ids),
                ('partner_id', '=', sel.partner_id.id),
                ('company_id', '=', sel.company_id.id)
            ]).ids
        tree_view = self.env.ref('account.invoice_tree')
        form_view = self.env.ref('account.invoice_form')
        return {
            'name': _('Account Invoice'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': tree_view.id,
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', invoice_ids)],
        }

    @api.multi
    def _get_quantity_max(self):
        for sel in self:
            sel.quantity_max = sum(
                [line.unit_amount for line in
                    self.env['account.analytic.line'].search([
                        ('contract_id', '=', sel.id),
                        ('contract_hours', '=', True)
                        ]
                    )]
                )

    @api.multi
    def _get_hours_quantity(self):
        for sel in self:
            sel.hours_quantity = sum(
                [line.unit_amount for line in
                    self.env['account.analytic.line'].search([
                        ('contract_id', '=', sel.id),
                        ('move_id', 'in', (False, None)),
                        ('billable', '=', True)
                        ]
                    )]
                )

    @api.multi
    def _get_remaining_hours(self):
        for sel in self:
            sel.remaining_hours = sel.quantity_max - sel.hours_quantity

    def _compute_attachment_ids(self):
        for sel in self:
            attachment_ids = self.env['ir.attachment'].search([
                ('res_id', '=', sel.id),
                ('res_model', '=', 'project.contract')
            ]).ids
            # from mail_thread
            message_attachment_ids =\
                self.mapped('message_ids.attachment_ids').ids
            sel.attachment_ids =\
                list(set(attachment_ids) - set(message_attachment_ids))

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].\
               next_by_code('sequence.project.contract') or '/'
        res = super(ProjectContract, self).create(vals)
        return res

    @api.multi
    def set_pending(self):
        self.write({'state': 'pending'})

    @api.multi
    def set_close(self):
        self.write({'state': 'close'})

    @api.multi
    def set_open(self):
        self.write({'state': 'open'})

    @api.multi
    def set_cancel(self):
        self.write({'state': 'cancelled'})

    def cron_account_analytic_account(self):
        def is_overdue_quantity(contract):
            if contract.quantity_max > 0.00:
                return contract.hours_quantity > contract.quantity_max
        base_url =\
            self.env['ir.config_parameter'].get_param('web.base.url')
        action_id =\
            self.env['ir.model.data'].get_object_reference(
                'project_contracts',
                'action_project_contracts')[1]
        menu_id = self.env.ref('project.menu_main_pm', False).id
        for contract in self.search([
             ('state', '=', 'open')
           ]):
            if is_overdue_quantity(contract):
                contract.state = 'pending'
        template = self.env.ref(
            'project_contracts.project_contract_cron_email_template', False)
        for user_id in list(set(
           [x.manager_id.id for x in self.search([('state', '=', 'pending')])]
           )):
            template.sudo().with_context(
                base_url=base_url,
                action_id=action_id,
                menu_id=menu_id
            ).send_mail(user_id, force_send=True)
