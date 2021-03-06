# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# Copyright (c) 2018 QubiQ (http://www.qubiq.es)

from openupgradelib import openupgrade


def create_project_contracts(env):
    # Check enterprise
    env.cr.execute("""Select EXISTS(
        SELECT relname FROM pg_class WHERE relname = 'sale_subscription')
    """)
    subscription_table = env.cr.dictfetchall()[0]['exists']
    query_subscription =\
        "select array_agg(id) as ids from sale_subscription where partner_id "
    env.cr.execute("""
        select array_agg(acc.id) as id_acc, array_agg(pp.id) as id_pp,
                acc.company_id as company_id, acc.partner_id as partner_id
        from project_project pp,
            (select id, name, partner_id, company_id
            from account_analytic_account
            order by partner_id desc) acc
        where pp.analytic_account_id = acc.id
        group by partner_id, company_id
        having acc.partner_id is not Null
        order by partner_id;
    """)
    contract = env['project.contract']
    partner = env['res.partner']
    query_max_acc =\
        "select state,date,user_id from account_analytic_account where id = "
    query_min_acc =\
        "select date_start from account_analytic_account where id = "

    for row in env.cr.dictfetchall():
        env.cr.execute(query_max_acc+str(max(list(row['id_acc']))))
        acc_max = env.cr.dictfetchall()
        env.cr.execute(query_min_acc+str(min(list(row['id_acc']))))
        acc_min = env.cr.dictfetchall()
        env['project.project'].sudo().browse(list(row['id_pp'])).write(
            {'active': True}
        )
        state = acc_max[0]['state']
        if state in ('draft', 'new', '', False, None):
            state = 'open'
        vals_pc = {
            'name': partner.browse(row['partner_id']).name,
            'partner_id': row['partner_id'],
            'project_ids': [(6, 0, list(row['id_pp']))],
            'manager_id': acc_max[0]['user_id'],
            'date_start': acc_min[0]['date_start'],
            'date_end': acc_max[0]['date'],
            'state': state,
            'company_id': row['company_id'],
        }
        contract = contract.create(vals_pc)
        # Change the messages
        aac_ids = contract.project_ids.mapped('analytic_account_id').ids
        if aac_ids:
            for notification in env['mail.message'].sudo().search([
                ('model', '=', 'account.analytic.account'),
                ('res_id', 'in', aac_ids),
               ]):
                notification.write({
                    'model': 'project.contract',
                    'res_id': contract.id,
                })
            if subscription_table:
                env.cr.execute(
                    query_subscription+'='+str(contract.partner_id.id))
                ss_ids = env.cr.dictfetchall()[0]['ids']
                if ss_ids:
                    ss_ids = list(ss_ids)
                    for notifcacion in env['mail.message'].sudo().search([
                        ('model', '=', 'sale.subscription'),
                        ('res_id', 'in', ss_ids)
                       ]):
                        notification.write({
                            'model': 'project.contract',
                            'res_id': contract.id,
                        })


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, 'account_analytic_account'):
        if openupgrade.table_exists(env.cr, 'project_project'):
            create_project_contracts(env)
