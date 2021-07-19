import unittest

from hex import HexCoord


class HexCoordTest(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(HexCoord(1, -1, 0) + HexCoord(2, 1, -3), HexCoord(3, 0, -3))
        self.assertEqual(HexCoord(-1, 0, 1) + HexCoord(1, 1, -2), HexCoord(0, 1, -1))

        self.assertEqual(HexCoord(-2, 1, 1) - HexCoord(0, 1, -1), HexCoord(-2, 0, 2))
        self.assertEqual(HexCoord(3, 4, -7) - HexCoord(2, 2, -4), HexCoord(1, 2, -3))

        self.assertEqual(HexCoord(-2, -1, 3) * 2, HexCoord(-4, -2, 6))
        self.assertEqual(HexCoord(0, -1, 1) * -1, HexCoord(0, 1, -1))

        self.assertEqual(HexCoord(-1, -2, 3) / 2, HexCoord(-0.5, -1, 1.5))
        self.assertEqual(HexCoord(0, -1, 1) / -4, HexCoord(0, 0.25, -0.25))

    def test_rounding(self):
        self.assertEqual(round(HexCoord(-0.9, -1, 1.9)), HexCoord(-1, -1, 2))
        self.assertEqual(round(HexCoord(1, -1.5, 0.5)), HexCoord(1, -1, 0))
        self.assertEqual(round(HexCoord(0.222, 1.1, -1.322)), HexCoord(0, 1, -1))
        self.assertEqual(round(HexCoord(0, 0.5, -0.5)), HexCoord(0, 0, 0))


if __name__ == '__main__':
    unittest.main()
