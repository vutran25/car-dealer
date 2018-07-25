"""
All unit tests.
"""
import unittest
from tests import agent


MDOULES = [
    agent
]


class Test(unittest.TestCase):
    """
    Run all tests.
    """
    for module in MDOULES:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        unittest.TextTestRunner(verbosity=2).run(suite)
