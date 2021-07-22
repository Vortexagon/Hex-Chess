import unittest

from pixel import PixelCoord


class PixelCoordTest(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(PixelCoord(1, 2) + PixelCoord(0, 5), PixelCoord(1, 7))
        self.assertEqual(PixelCoord(-3, 3) + PixelCoord(2, 1), PixelCoord(-1, 4))

        self.assertEqual(PixelCoord(3, 1) - PixelCoord(-1, 3), PixelCoord(4, -2))
        self.assertEqual(PixelCoord(7, -5) - PixelCoord(3, -1), PixelCoord(4, -4))

        self.assertEqual(PixelCoord(1, -2) * 5, PixelCoord(5, -10))
        self.assertEqual(PixelCoord(4, -6) * -3, PixelCoord(-12, 18))

        self.assertEqual(PixelCoord(8, 0) / 2, PixelCoord(4, 0))
        self.assertEqual(PixelCoord(2, -3) / -1, PixelCoord(-2, 3))


if __name__ == '__main__':
    unittest.main()
