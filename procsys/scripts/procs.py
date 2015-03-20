#
# This file is part of ProcSys.

# ProcSys is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# ProcSys is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ProcSys.  If not, see <http://www.gnu.org/licenses/>.

'''ps-like script to dump processes information.'''

import sys

from argparse import ArgumentParser, ArgumentTypeError

from procsys.process.collection import Collection, Collector
from procsys.process.filter import CommandLineFilter
from procsys.process.formatters import get_formats, get_formatter


def get_parser():
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
    return parser


def main():
    args = get_parser().parse_args()
    fields = [field.strip() for field in args.fields.split(',')]

    collector = Collector(pids=args.pids)
    collection = Collection(collector=collector)
    if args.regexp:
        collection.add_filter(CommandLineFilter(args.regexp))
    formatter_class = get_formatter(args.format)
    formatter = formatter_class(sys.stdout, fields)
    formatter.format(collection)
