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

'''Filter classes for process Collection.'''

import re


class CommandLineFilter(object):
    '''Filter Processes based on the command line.

    Parameters:
      regexp: a regexp to match the commandline.
      include_args: whether include args in match.

    '''

    def __init__(self, regexp, include_args=False):
        self._re = re.compile(regexp)
        self._include_args = include_args

    def __call__(self, process):
        cmd = process.cmd
        if not self._include_args:
            cmd = cmd.split()[0]
        return bool(self._re.findall(cmd))
