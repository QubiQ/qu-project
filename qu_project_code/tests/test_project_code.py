# -*- coding: utf-8 -*-
# Copyright 2018 QubiQ <marsal.isern@qubiq.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.tests.common as common

# TO DO !!


class TestProjectCode(common.TransactionCase):

    def setUp(self):
        super(TestProjectCode, self).setUp()
        self.project_model = self.env['project.project']
        self.ir_sequence_model = self.env['ir.sequence']
        self.project_sequence = self.env.ref('qu_project_code.sequence_project')
        self.project_task = self.env.ref('project.project_task_1')

    def test_old_task_code_assign(self):
        projects = self.project_model.search([])
        for project in projects:
            self.assertNotEqual(project.code, '/')

    def test_new_task_code_assign(self):
        number_next = self.project_sequence.number_next_actual
        code = self.project_sequence.get_next_char(number_next)
        project_task = self.project_model.create({
            'name': 'Testing Prooject Code code',
        })
        self.assertNotEqual(project_task.code, '/')
        self.assertEqual(project_task.code, code)

    def test_copy_task_code_assign(self):
        number_next = self.task_sequence.number_next_actual
        code = self.task_sequence.get_next_char(number_next)
        project_task_copy = self.project_task.copy()
        self.assertNotEqual(project_task_copy.code, self.project_task.code)
        self.assertEqual(project_task_copy.code, code)
