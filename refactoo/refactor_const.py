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
from comby import Comby


def refactor_const(opts: argparse.Namespace, text: str) -> str:
    comby = Comby()

    # Move const to the middle
    text = comby.rewrite(text, "const :[a:e]&", ":[a] const&")
    text = comby.rewrite(text, "const :[a:e]*", ":[a] const*")

    # Cleanup some spaces
    text = comby.rewrite(text, "const :[a:e] &", ":[a] const&")
    text = comby.rewrite(text, "const :[a:e] *", ":[a] const*")

    return text


# EOF #
