# -*- coding: utf-8 -*-
"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import click

from croncheck.common.exceptions import CronConfigExeption
from croncheck.common.utils import (parse_time_check_argument, parse_config,
                                    get_running_time)


@click.command(help='Checking Cron Config\n')
@click.argument('checking_time')
def cron_check(checking_time):
    try:
        time_to_check = parse_time_check_argument(checking_time)
        std_in = click.get_text_stream('stdin')
        for line in std_in:
            try:
                parsed_config = parse_config(line)
            except CronConfigExeption as e:
                print(e)
            else:
                running_time = get_running_time(parsed_config[:2], time_to_check)
                print('{} {} - {}'.format(running_time[0], running_time[1], parsed_config[2]))

    except Exception as e:
        print(e)
        exit(2)


if __name__ == '__main__':  # pragma: no cover
    cron_check()
