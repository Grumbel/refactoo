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


import argparse
import unittest

from refactoo.refactor_const import refactor_const


class RefactorConstTestCase(unittest.TestCase):

    def test_refactor_const(self) -> None:
        test_data = [(
            r"""
            void foobar(const Foobar& foo) {}
            void foobar(const Foobar* foo) {}
            """,
            r"""
            void foobar(Foobar const& foo) {}
            void foobar(Foobar const* foo) {}
            """
        )]

        for source, expected_result in test_data:
            self.assertEqual(refactor_const(argparse.Namespace(), source),
                             expected_result)


# EOF #
