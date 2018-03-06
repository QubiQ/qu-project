# -*- coding: utf-8 -*-
# Copyright 2017 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestProjectStageValidator(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestProjectStageValidator, self).setUp(*args, **kwargs)
        self.project = self.env['project.project']
        self.project_task = self.env['project.task']
        self.project_issue = self.env['project.issue']
        self.project_stage = self.env['project.task.type']
        self.user = self.env['res.users']

        # Create a validator user and a 'normal' user
        self.validator_user = self.user.create({
                'name': 'Validator',
                'login': 'validator',
            })
        self.not_validator_user = self.user.create({
                'name': 'NOT validator',
                'login': 'not_validator',
            })
        # Add only the validator user
        self.test_project = self.project.create({
                'name': 'Project Test',
                'partner_id': 1,
                'use_tasks': True,
                'use_issues': True,
                'validators_ids': [(6, 0, [self.validator_user.id])],
            })
        self.test_task1 = self.project_task.create({
                'name': 'Task Test 1',
                'project_id': self.test_project.id,
            })
        self.test_task2 = self.project_task.create({
                'name': 'Task Test 2',
                'project_id': self.test_project.id,
            })
        self.test_issue1 = self.project_issue.create({
                'name': 'Issue Test 1',
                'project_id': self.test_project.id,
            })
        self.test_issue2 = self.project_issue.create({
                'name': 'Issue Test 2',
                'project_id': self.test_project.id,
            })
        # Mark the stage 'Test' as a validable stage, that way,
        # only the 'Validator' user will be able to move
        # tasks and issues to this stage
        self.test_stage = self.project_stage.create({
                'name': 'Test',
                'needs_validator': True,
                'project_ids': [(6, 0, [self.test_project.id])],
            })

    def test_task_validator(self):
        ctx = {
            'uid': self.validator_user.id,
        }
        self.test_task1.with_context(ctx).write({
                'stage_id': self.test_stage.id,
            })
        self.assertEqual(self.test_task1.stage_id.id, self.test_stage.id)

    def test_task_not_validator(self):
        with self.assertRaises(ValidationError):
            ctx = {
                'uid': self.not_validator_user.id,
            }
            self.test_task2.with_context(ctx).write({
                    'stage_id': self.test_stage.id,
                })

    def test_issue_validator(self):
        ctx = {
            'uid': self.validator_user.id,
        }
        self.test_issue1.with_context(ctx).write({
                'stage_id': self.test_stage.id,
            })
        self.assertEqual(self.test_issue1.stage_id.id, self.test_stage.id)

    def test_issue_not_validator(self):
        with self.assertRaises(ValidationError):
            ctx = {
                'uid': self.not_validator_user.id,
            }
            self.test_issue2.with_context(ctx).write({
                    'stage_id': self.test_stage.id,
                })
