#
# This file is part of ProcSys.
#
# ProcSys is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''ps-like script to dump processes information.'''

import sys
from itertools import repeat
from time import sleep
from argparse import ArgumentParser, ArgumentTypeError

from toolrack.script import Script

from procsys.process.collection import Collection, Collector
from procsys.process.filter import CommandLineFilter
from procsys.process.formatters import get_formats, get_formatter


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
            '--regexp', '-r', help='regexp to filter commandline')
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
        formatter_class = get_formatter(args.format)
        formatter = formatter_class(sys.stdout, fields)

        count_iter = range(args.count) if args.count else repeat(None)
        for n in count_iter:
            formatter.format(collection)
            if n != args.count - 1:
                # don't sleep after last iteration
                sleep(args.interval)


script = ProcsScript()
