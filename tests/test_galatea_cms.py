# This file is part of the galatea_cms module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class GalateaCmsTestCase(ModuleTestCase):
    'Test Galatea Cms module'
    module = 'galatea_cms'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        GalateaCmsTestCase))
    return suite