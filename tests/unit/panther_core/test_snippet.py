"""
Panther Analysis Tool is a command line interface for writing,
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

"""Unit tests for src/policy.py"""
import unittest

from panther_core.snippet import Snippet


class TestSnippet(unittest.TestCase):
    """Unit tests for policy.Policy"""

    def test_prefilter_snippet_success(self) -> None:
        snipper = Snippet(
            {
                'id': 'test_snippet',
                'type': 'Panther::PreFilter',
                'when': {
                    'condition': 'Equals',
                    'key': 'my-key',
                    'value': 'my-value'
                }
            }
        )

        self.assertFalse(snipper.prefilter({'my-key': 'does-not-match'}))
        self.assertTrue(snipper.prefilter({'my-key': 'my-value'}))

    def test_prefilter_snippet_missing_fields(self) -> None:
        with self.assertRaises(AssertionError):
            _ = Snippet(
                {
                    'id': 'test_snippet',
                    'when': {
                        'condition': 'Equals',
                        'key': 'my-key',
                        'value': 'my-value'
                    }
                }
            )
