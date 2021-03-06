# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from unittest import TestCase

from click.testing import CliRunner

from croncheck.app import cron_check


class CronCheckTestCase(TestCase):
    """Test suite for croncheck command-line interfaces."""
    def setUp(self):
        self.runner = CliRunner()

    def test_croncheck_without_time_check_argument(self):
        result = self.runner.invoke(cron_check, [])
        self.assertEqual(2, result.exit_code)

    def test_croncheck_works_correctly(self):
        sample_stdin = '* 12 test_command_1\n' \
                       '  * * test_command_2\n' \
                       '24 10 test_command_3\n' \
                       '62 11 test_command_4\n'

        result = self.runner.invoke(cron_check, args=['11:22'], input=sample_stdin)
        self.assertEqual(0, result.exit_code)
        self.assertIn('12:00 today - test_command_1', result.output)
        self.assertIn('11:22 today - test_command_2', result.output)
        self.assertIn('10:24 tomorrow - test_command_3', result.output)


    def test_croncheck_with_invalid_time_check_argument(self):
        invalid_args = ('1:22', '12:1', 'aa:bb', '11:cc', '24:11', '12:60', '25:74')
        for arg in invalid_args:
            result = self.runner.invoke(cron_check, args=[arg])
            self.assertEqual(2, result.exit_code)
