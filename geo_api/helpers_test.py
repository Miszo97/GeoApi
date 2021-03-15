import unittest

from helpers import getIP


class TestGetIP(unittest.TestCase):
    def test_correct_address(self):
        correct_address = 'www.google.com'

        self.assertTrue(isinstance(getIP(correct_address), str))

    def test_incorrect_address(self):
        incorrect_adress = 'adrress'

        self.assertEqual(getIP(incorrect_adress), False)


if __name__ == "__main__":
    unittest.main()
