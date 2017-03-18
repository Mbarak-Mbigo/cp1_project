"""Amity test suite.

tests/test.py

Process:
    Write a failing unit test
    Make the unit test pass
    Refactor
"""
# imports
import unittest

# local imports
from app.amity import Amity


class AmityTests(unittest.TestCase):
    """Test Suite for Amity."""

    # fixtures
    def setUp(self):
        """Create necessary objects."""
        self.amity = Amity()

    def tearDown(self):
        """Create necessary objects."""
        del self.amity

    def test_creates_room(self):
        """Test rooms are created successfullly."""
        # captures invalid input: type(office|living), room: list
        # test prevents creating abstract room
        # test room number increases
        # test creates living rooms, one and multiple
        # test crates office rooms, one and multiple
        pass
