# -*- coding: utf-8 -*-

import unittest
from rawdisk.util.output import format_table

class TestOutputModule(unittest.TestCase):
    def test_format_table_returns_valid_rows(self):
        values = [
            type('obj', (object,),
                 {'prop1': 'VAL1', 'prop2': 'VAL2', 'prop3': 'VAL3'}),
            type('obj', (object,),
                 {'prop1': 'VAL1 LONG', 'prop2': 'VAL2', 'prop3': 'VAL3'})
        ]

        expected = [
            'COL1       COL2  LONG_COL_3',
            '---------  ----  ----------',
            'VAL1       VAL2  VAL3      ',
            'VAL1 LONG  VAL2  VAL3      ',
        ]

        actual = format_table(
            ['COL1', 'COL2', 'LONG_COL_3'],
            ['prop1', 'prop2', 'prop3'],
            values
        )

        self.assertEqual(actual, expected)
