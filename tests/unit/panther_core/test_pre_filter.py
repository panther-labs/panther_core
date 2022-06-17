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

"""Unit tests for panther_core/pre_filter.py"""
import unittest

from panther_core.pre_filter import (
    CONTAINS,
    EQUALS,
    GREATER_THAN,
    GREATER_THAN_EQUAL,
    LESS_THAN,
    LESS_THAN_EQUAL,
    AND,
    IN,
    NOT,
    OR,
    PreFilter,
)

class TestPreFilter(unittest.TestCase):
    """Unit tests for panther_core.pre_filter"""

    def test_pre_filter_and(self) -> None:
        filter = PreFilter(
            {
                AND: [
                    {
                        'key': 'my-key',
                        'value': 'my-value',
                        'condition': EQUALS,
                    },
                    {
                        'key': 'my-other-key',
                        'condition': IN,
                        'value': [1,2,3,5,8]
                    }
                ]
            }
        )

        # test matching case
        test_event = {
            'my-key': 'my-value',
            'my-other-key': 3,
        }
        self.assertTrue(filter.filter(test_event))

        # test non-matching-case
        test_event['my-other-key'] = 0
        self.assertFalse(filter.filter(test_event))


    def test_pre_filter_or(self) -> None:
        filter = PreFilter(
            {
                OR: [
                    {
                        'key': 'my-key',
                        'value': 'my-value',
                        'condition': EQUALS,
                    },
                    {
                        'key': 'my-other-key',
                        'condition': IN,
                        'value': [1,2,3,5,8]
                    }
                ]
            }
        )

        # test matching case
        test_event = {
            'my-key': 'my-value',
            'my-other-key': 0,
        }
        self.assertTrue(filter.filter(test_event))

        # test non-matching-case
        test_event['my-key'] = 0
        self.assertFalse(filter.filter(test_event))

    def test_pre_filter_not(self) -> None:
        filter = PreFilter(
            {
                NOT: [
                    {
                        'key': 'my-key',
                        'value': 'my-value',
                        'condition': EQUALS,
                    },
                ]
            }
        )

        # test matching case
        test_event = {
            'my-key': 'not-my-value',
        }
        self.assertTrue(filter.filter(test_event))

        # test non-matching-case
        test_event['my-key'] = 'my-value'
        self.assertFalse(filter.filter(test_event))

    def test_pre_filter_differing_types(self) -> None:
        filter = PreFilter(
            {
                'key': 'my-key',
                'value': 'my-value',
                'condition': EQUALS,
            }
        )
        # test matching case
        test_event = {
            'my-key': ['test'],
        }
        self.assertFalse(filter.filter(test_event))

    def test_pre_filter_basic_comparisons(self) -> None:
        filter = PreFilter(
            {
                AND: [
                    {
                        'key': 'equal',
                        'value': 'my-value',
                        'condition': EQUALS,
                    },
                    {
                        'key': 'greater-than',
                        'value': 30,
                        'condition': GREATER_THAN,
                    },
                    {
                        'key': 'greater-than-equal',
                        'value': 30,
                        'condition': GREATER_THAN_EQUAL,
                    },
                    {
                        'key': 'less-than',
                        'value': 30,
                        'condition': LESS_THAN,
                    },
                    {
                        'key': 'less-than-equal',
                        'value': 30,
                        'condition': LESS_THAN_EQUAL,
                    },
                    {
                        'key': 'in',
                        'condition': IN,
                        'value': [1,2,3,5,8]
                    },
                    {
                        'key': 'contains',
                        'condition': CONTAINS,
                        'value': 'world',
                    },

                ]
            }
        )
        # test matching case
        test_event = {
            'equal': 'my-value',
            'greater-than': 31,
            'greater-than-equal': 30,
            'less-than': 29,
            'less-than-equal': 30,
            'in': 2,
            'contains': "hello-world"
        }
        self.assertTrue(filter.filter(test_event))
        # test non-matching case
        test_event['in'] = 10
        self.assertFalse(filter.filter(test_event))
