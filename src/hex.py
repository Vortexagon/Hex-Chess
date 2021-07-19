class HexCoord:
    def __init__(self, p, q, r):
        assert p + q + r <= 1e-6  # p + q + r should equal 0, but this is to account for floating-point error.
        self.p, self.q, self.r = p, q, r
