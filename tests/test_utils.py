# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from unittest import TestCase

from faker import Faker

from croncheck.common.exceptions import TimeCheckArgumentException, CronConfigExeption
from croncheck.common.utils import parse_time_check_argument, parse_config, get_running_time


_FAKE = Faker()


class UtilsTestCase(TestCase):
    def test_parsing_time_check_argument(self):
        sample_hour = _FAKE.time(pattern="%H")
        sample_minute = _FAKE.time(pattern="%M")
        sample_time = '{}:{}'.format(sample_hour, sample_minute)
        self.assertTupleEqual(parse_time_check_argument(sample_time),
                              (int(sample_hour), int(sample_minute)))

    def test_raising_exception_if_invalid_arguement(self):
        invalid_arguments = ('1:12', '12:1', '12', 'HELLO', 'AA:BB', '12:13:14', None, '24:01',
                             '12:63', '27:72')

        for argument in invalid_arguments:
            with self.assertRaises(TimeCheckArgumentException):
                parse_time_check_argument(argument)

    def test_raising_exception_if_invalid_config(self):
        invalid_configs = ('* 2', '1 aa test command',
                           '* 25 test command',
                           '60 12 test command', '60 24 test command')
        for cron_config in invalid_configs:
            with self.assertRaises(CronConfigExeption):
                parse_config(cron_config)

    def test_parse_config(self):
        sample_configs = [(_FAKE.random_int(0, 59), _FAKE.random_int(0, 24), _FAKE.sentence()),
                          ('*', _FAKE.random_int(0, 24), _FAKE.sentence()),
                          (_FAKE.random_int(0, 59), '*', _FAKE.sentence()),
                          ('*', '*', _FAKE.sentence())]

        for test_min, test_hour, test_command in sample_configs:
            cron_config = '{} {} {}'.format(test_min, test_hour, test_command)
            expected_parsed = (test_min, test_hour, test_command)
            self.assertTupleEqual(expected_parsed, parse_config(cron_config))

    def test_get_running_time(self):
        # sample_cron(M, H), sample_time_to_check(H, M), expected_result (TIME, DAY)
        samples = [((10, 8), (8, 11), ('8:10', 'tomorrow')),
                   ((10, 8), (8, 9), ('8:10', 'today')),
                   ((10, 8), (8, 10), ('8:10', 'today')),
                   ((10, 7), (8, 10), ('7:10', 'tomorrow')),
                   ((10, '*'), (8, 9), ('8:10', 'today')),
                   ((10, '*'), (8, 11), ('9:10', 'today')),
                   ((10, '*'), (23, 11), ('0:10', 'tomorrow')),
                   ((10, '*'), (8, 10), ('8:10', 'today')),
                   (('*', 8), (8, 10), ('8:10', 'today')),
                   (('*', 11), (8, 10), ('11:00', 'today')),
                   (('*', 2), (8, 10), ('2:00', 'tomorrow')),
                   (('*', '*'), (8, 10), ('8:10', 'today')),
                   ((2, 3), (1, 2), ('3:02', 'today'))]

        for sample_cron_time, sample_time_to_check, expected_result in samples:
            self.assertTupleEqual(expected_result,
                                  get_running_time(sample_cron_time, sample_time_to_check))
