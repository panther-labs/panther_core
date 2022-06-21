"""
Panther Core is a command line interface for writing,
testing, and packaging policies/rules.
Copyright (C) 2020 Panther Labs Inc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Dict

from .pre_filter import PreFilter


class Snippet:
    id: str
    type: str
    when: PreFilter

    def __init__(self, config: Dict):

        for each_field in ["id", "type"]:
            if not (each_field in config) or not isinstance(config[each_field], str):
                raise AssertionError('Field "%s" of type str is required field' % each_field)

        self.id = config['id']
        self.type = config['type']
        self.when = PreFilter(config.get('when', {}))

    def prefilter(self, event: Dict) -> bool:
        return self.when.filter(event)
