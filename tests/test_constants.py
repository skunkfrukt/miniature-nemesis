from src.constants import *
import unittest

class TestConstants(unittest.TestCase):
    def setUp(self):
        # A small bit range.
        self.bits = tuple(bitrange(3))

    def test_first_bit(self):
        self.assertEqual(1, self.bits[0])

    def test_second_bit(self):
        self.assertEqual(2, self.bits[1])

    def test_third_bit(self):
        self.assertEqual(4, self.bits[2])

    def test_no_fourth_bit(self):
        with self.assertRaises(IndexError):
             self.bits[3]
