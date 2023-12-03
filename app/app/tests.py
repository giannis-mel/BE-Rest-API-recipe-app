"""
Sample tests
"""
from django.test import SimpleTestCase
# No db integration

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""

    def test_add_numbers(self):
        """Test adding numbers together."""
        self.assertEqual(11, calc.add(5, 6))

    def test_subtract_numbers(self):
        """Test subtracting numbers."""
        self.assertEqual(5, calc.subtract(10, 15))
