class HexCoord:
    def __init__(self, p, q, r):
        assert p + q + r <= 1e-6  # p + q + r should equal 0, but this is to account for floating-point error.
        self.p, self.q, self.r = p, q, r

    def __add__(self, other):
        return HexCoord(self.p + other.p, self.q + other.q, self.r + other.r)

    def __sub__(self, other):
        return HexCoord(self.p - other.p, self.q - other.q, self.r - other.r)

    def __mul__(self, other):
        return HexCoord(self.p * other, self.q * other, self.r * other)

    def __truediv__(self, other):
        return HexCoord(self.p / other, self.q / other, self.r / other)

    def __eq__(self, other):
        if type(other) is not type(self):
            return False

        return self.p == other.p and self.q == other.q and self.r == other.r
