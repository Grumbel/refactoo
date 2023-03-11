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


import re


def refactor_log(content: str) -> str:
    replacements = []

    # FIXME: fails when ';' is in the string
    # FIXME: fails when logging uses a linebreak with '\'

    for match in re.findall(r'log_(?:warning|info|debug|fatal)[^;]*', content, re.MULTILINE):
        tokens = [x.strip() for x in match.split("<<")]
        fmttext = ""
        args = []
        for token in tokens[1:]:
            if token.startswith('"') and token.endswith('"'):
                fmttext += token[1:-1]
            elif token == "std::endl":
                pass
            else:
                fmttext += "{}"
                args.append(token)

        argstext = ", ".join(args)

        original = match
        if argstext == "":
            replacement = f"{tokens[0]}(\"{fmttext}\")"
        else:
            replacement = f"{tokens[0]}(\"{fmttext}\", {argstext})"

        replacements.append((original, replacement))

    newcontent = content
    for (orig, repl) in replacements:
        newcontent = newcontent.replace(orig, repl)

    return newcontent


# EOF #
