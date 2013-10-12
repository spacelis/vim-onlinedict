#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: test_connectors.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:
    tests
"""

import unittest

from connectors.dictionaries import OxfordDictionaries


class TestConnectors(unittest.TestCase):

    def test_oxford_dictionaries(self):
        """@todo: Docstring for test_oxford_dictionaries.
        :returns: @todo

        """
        od = OxfordDictionaries()
        self.fail(od.query('requests'))
