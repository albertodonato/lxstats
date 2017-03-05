'''ps-like script to dump processes information.'''

import sys
from itertools import repeat
from time import sleep
from argparse import ArgumentParser, ArgumentTypeError

from toolrack.script import Script

from ..process.collection import Collection, Collector
from ..process.filter import CommandLineFilter
from ..process.formatters import get_formats, get_formatter


class ProcsScript(Script):
    '''ps-like utility.

    It supports commandline-based filtering and output in different formats.

    '''

    def get_parser(self):
        parser = ArgumentParser(
            description='Dump info about running processes.')

        def pids(pid_list):
            '''Comma-separated list of PIDs.'''
            try:
                return [int(pid) for pid in pid_list.split(',')]
            except:
                raise ArgumentTypeError('Must specify a list of PIDs')

        parser.add_argument(
            '--fields', '-f',
            help='comma-separated list of fields to display',
            default='pid,stat.state,comm')
        parser.add_argument(
            '--regexp', '-r', help='regexp to filter by process name')
        parser.add_argument(
            '--cmdline-regexp', '-R',
            help='regexp to filter by full command line')
        parser.add_argument(
            '--pids', '-p', help='list specific PIDs', type=pids)
        parser.add_argument(
            '--format', '-F', help='output format', choices=get_formats(),
            default='table')
        parser.add_argument(
            '--interval', '-i',
            help='sample interval in seconds (default %(default)s)', type=int,
            default=5)
        parser.add_argument(
            '--count', '-c',
            help='number of samples to collect (default unlimited)', type=int,
            default=0)
        return parser

    def main(self, args):
        fields = [field.strip() for field in args.fields.split(',')]

        collector = Collector(pids=args.pids)
        collection = Collection(collector=collector)
        if args.regexp:
            collection.add_filter(CommandLineFilter(args.regexp))
        if args.cmdline_regexp:
            collection.add_filter(
                CommandLineFilter(args.cmdline_regexp, include_args=True))
        formatter_class = get_formatter(args.format)
        formatter = formatter_class(sys.stdout, fields)

        count_iter = range(args.count) if args.count else repeat(None)
        for n in count_iter:
            formatter.format(collection)
            if n != args.count - 1:
                # don't sleep after last iteration
                sleep(args.interval)


script = ProcsScript()
