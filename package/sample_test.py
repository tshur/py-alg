import unittest

from package import sample


class SampleTest(unittest.TestCase):
    def test_square(self):
        self.assertEqual(sample.square(0), 0)
        self.assertEqual(sample.square(1), 1)
        self.assertEqual(sample.square(2), 4)
        self.assertEqual(sample.square(5), 25)
        self.assertEqual(sample.square(-5), 25)


if __name__ == "__main__":
    unittest.main()
