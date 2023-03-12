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
import difflib

from refactoo.refactor_log import refactor_log
from refactoo.refactor_const import refactor_const
from refactoo.refactor_include_guards import refactor_include_guards


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Replace log_... with fmt::format')

    parser.add_argument('--in-place', action='store_true', default=False,
                        help='modify files in-place')

    parser.add_argument('--diff', action='store_true', default=False,
                        help='show diff of changes')

    subparsers = parser.add_subparsers()

    refactor_log_parser = subparsers.add_parser("log")
    refactor_log_parser.set_defaults(filter_func=refactor_log)

    refactor_const_parser = subparsers.add_parser("const")
    refactor_const_parser.set_defaults(filter_func=refactor_const)

    refactor_include_guards_parser = subparsers.add_parser("include-guards")
    refactor_include_guards_parser.add_argument("--project", type=str, required=True)
    refactor_include_guards_parser.set_defaults(filter_func=refactor_include_guards)

    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='input files to be processed')

    return parser.parse_args()


def main():
    opts = parse_args()

    for filename in opts.files:
        with open(filename, 'r', encoding='utf-8') as fin:
            content = fin.read()
            newcontent = opts.filter_func(opts, content)

        if opts.diff:
            for difference in difflib.unified_diff(content.splitlines(),
                                                   newcontent.splitlines(),
                                                   filename + ".old",
                                                   filename + ".new"):
                if difference[0] != " ":
                    print(difference)
        elif opts.in_place:
            with open(filename, 'w', encoding='utf-8') as fout:
                fout.write(newcontent)
        else:
            sys.stdout.write(newcontent)


if __name__ == "__main__":
    main()


# EOF #
