import math


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

    def __round__(self, n=None):
        rp = round(self.p)
        rq = round(self.q)
        rr = round(self.r)

        p_diff = abs(self.p - rp)
        q_diff = abs(self.q - rq)
        r_diff = abs(self.r - rr)

        diff_list = [p_diff, q_diff, r_diff]

        if max(diff_list) == p_diff:
            rp = -(rq + rr)
        elif max(diff_list) == q_diff:
            rq = -(rp + rr)
        else:
            rr = -(rp + rq)

        return HexCoord(rp, rq, rr)

    def __str__(self):
        return f"({self.p}, {self.q}, {self.r})"

    def __hash__(self):
        return hash((1 * self.p, 2 * self.q, 3 * self.r))


class HexCell:
    def __init__(self, coord, state=None):
        self.coord = coord
        self.state = state


class HexMap:
    def __init__(self, cells=None):
        if cells is None: cells = dict()
        self.cells = cells

    @staticmethod
    def from_radius(radius):
        cells = dict()
        for p in range(-radius, radius + 1):
            for q in range(-radius, radius + 1):
                for r in range(-radius, radius + 1):
                    if p + q + r == 0:
                        coord = HexCoord(p, q, r)
                        cells[coord] = HexCell(coord)
        return HexMap(cells)

    def __iter__(self):
        return self.cells.values()

    def __getitem__(self, item):
        return self.cells[item].state

    def __setitem__(self, key, value):
        self.cells[key].state = value


class HexPixelAdapter:
    def __init__(self, dimensions, origin, hex_radius):
        self.dimensions = dimensions
        self.origin = origin
        self.hex_radius = hex_radius

    def hex_to_pixel(self, coord):
        x = self.hex_radius * 1.5 * coord.p + self.origin[0]
        y = self.hex_radius * (math.sqrt(3) * 0.5 * coord.p + math.sqrt(3) * coord.r) + self.origin[1]

        return x, y

    def pixel_to_hex(self, coord):
        coord = (coord[0] - self.origin[0], coord[1] - self.origin[1])

        p = (2/3) * coord[0] / self.hex_radius
        r = (-1/3.0 * coord[0] + math.sqrt(3)/3.0 * coord[1]) / self.hex_radius

        return HexCoord(p, -p-r, r)

    def get_vertices(self, coord):
        x, y = self.hex_to_pixel(coord)
        angle = math.pi / 3

        return [(
            self.hex_radius * math.cos(angle * i) + x,
            self.hex_radius * math.sin(angle * i) + y
        ) for i in range(6)]
