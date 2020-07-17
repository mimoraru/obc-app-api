from django.test import TestCase

from app.calc import add


class CalcTest(TestCase):
    def test_add_numbers(self):
        """Simple unit test for the addition of two numbers"""
        self.assertEquals(add(3, 8), 11)
        