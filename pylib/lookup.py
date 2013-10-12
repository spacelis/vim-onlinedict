#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lookup.py
Author: SpaceLis
Email: Wen.Li@tudelft.nl
GitHub: http://github.com/spacelis
Description:

"""

import sys
from connectors.dictionaries import OxfordDictionaries


od = OxfordDictionaries()
print od.query(sys.argv[1])
