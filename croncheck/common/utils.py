# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from croncheck.common.exceptions import TimeCheckArgumentException, CronConfigExeption


def _get_only_valid_time_or_star(input_string, validation):
    if validation == 'minutes':
        max_range = 60
    else:
        max_range = 24
    if input_string == '*':
        return '*'
    elif int(input_string) in range(0, max_range):
        return int(input_string)
    else:
        raise Exception()


def _validate_parsed_time_list(parsed_time_list):
    hour_int = int(parsed_time_list[0])
    min_int = int(parsed_time_list[1])

    if (len(parsed_time_list[0]) != 2 or
            len(parsed_time_list[1]) != 2 or
            hour_int not in range(0, 24) or
            min_int not in range(0, 60)):
        raise Exception()

    return hour_int, min_int


def parse_time_check_argument(time_check_string):
    exception_message = 'Invalid time format! syntax: HH:MM ( [00~23]:[00~59])'
    try:
        parsed_time_list = time_check_string.split(':')
        if len(parsed_time_list) != 2:
            raise Exception()
        parsed_time = _validate_parsed_time_list(parsed_time_list)
    except Exception:
        raise TimeCheckArgumentException(exception_message)

    return parsed_time


def parse_config(cron_config):
    exception_message = 'Invalid cron config:'

    try:
        parsed_config_list = cron_config.split()
        if len(parsed_config_list) < 3:
            raise Exception()
        parsed_config = (
            _get_only_valid_time_or_star(parsed_config_list[0], validation='minutes'),
            _get_only_valid_time_or_star(parsed_config_list[1], validation='hour'),
            ' '.join(parsed_config_list[2:])
        )

    except Exception:
        raise CronConfigExeption('%s %s' % (exception_message, cron_config.rstrip()))

    return parsed_config


def _get_minute_in_two_character(int_minute):
    if int_minute < 10:
        return '0{}'.format(int_minute)
    else:
        return str(int_minute)


def _get_running_day(run_hour, run_min, check_hour, check_min):
    if (run_hour > 23) or (run_hour < check_hour) or (
            run_hour == check_hour and run_min < check_min):
        return 'tomorrow'
    return 'today'


def get_running_time(cron_time, time_to_check):

    cron_hour = cron_time[1]
    cron_min = cron_time[0]
    check_hour = time_to_check[0]
    check_min = time_to_check[1]

    run_hour = cron_hour
    run_min = cron_min

    if cron_min == '*':
        run_min = check_min if cron_hour in [check_hour, '*'] else 0

    if cron_hour == '*':
        run_hour = check_hour + 1 if run_min < check_min else check_hour

    running_day = _get_running_day(run_hour, run_min, check_hour, check_min)

    if run_hour > 23:
        run_hour = run_hour - 24

    return '{}:{}'.format(run_hour, _get_minute_in_two_character(run_min)), running_day
