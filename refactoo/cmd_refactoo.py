# refactoo - C++ Refactoring Tools
# Copyright (C) 2023 Ingo Ruhnke <grumbel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import argparse

from refactoo.refactor_log import refactor_log


def parse_args():
    parser = argparse.ArgumentParser(description='Replace log_... with fmt::format')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='input files to be processed')
    parser.add_argument('--in-place', action='store_true', default=False,
                        help='modify files in-place')

    return parser.parse_args()


def main():
    opts = parse_args()

    for filename in opts.files:
        with open(filename, 'r', encoding='utf-8') as fin:
            content = fin.read()
            newcontent = refactor_log(content)

        if opts.in_place:
            with open(filename, 'w', encoding='utf-8') as fout:
                fout.write(newcontent)
        else:
            sys.stdout.write(newcontent)


if __name__ == "__main__":
    main()


# EOF #
