# Copyright 2019 Joan Segui <joan.segui@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class ModifyFollowersIssueWizard(models.TransientModel):
    _name = 'modify.followers.issue.wizard'

    follower_ids = fields.Many2many(
        comodel_name='res.partner',
        string=_('Followers'),
        default=lambda self: self.env['helpdesk.ticket'].browse(
            self._context.get('active_id')).message_partner_ids.ids
    )
    channel_ids = fields.Many2many(
        comodel_name='mail.channel',
        string=_('Channel'),
        default=lambda self: self.env['helpdesk.ticket'].browse(
            self._context.get('active_id')).message_channel_ids.ids
    )

    def modify_followers(self):
        active_id = self.env['helpdesk.ticket'].browse(
            self._context.get('active_id'))
        active_id.message_subscribe(
            partner_ids=list(
                set(self.follower_ids.ids) -
                set(active_id.message_partner_ids.ids)),
            channel_ids=list(
                set(self.channel_ids.ids) -
                set(active_id.message_channel_ids.ids))
        )
        active_id.message_unsubscribe(
            partner_ids=list(filter(lambda x: x not in self.follower_ids.ids,
                                    active_id.message_partner_ids.ids)),
            channel_ids=list(filter(lambda x: x not in self.channel_ids.ids,
                                    active_id.message_channel_ids.ids))
        )
