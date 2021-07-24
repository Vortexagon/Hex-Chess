import math

from pixel import PixelCoord


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

    def __abs__(self):
        return HexCoord(abs(self.p), abs(self.q), abs(self.r))


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

    @staticmethod
    def from_glinski():
        glinski_pos = {
            "w_pawn": [(-n, -1, n + 1) for n in range(5)] + [(n, -n - 1, 1) for n in range(5)],
            "w_rook": [(-3, -2, 5), (3, -5, 2)],
            "w_knight": [(-2, -3, 5), (2, -5, 3)],
            "w_bishop": [(0, -3, 3), (0, -4, 4), (0, -5, 5)],
            "w_queen": [(-1, -4, 5)],
            "w_king": [(1, -5, 4)],

            "b_pawn": [(-n, n + 1, -1) for n in range(5)] + [(n, 1, -n - 1) for n in range(5)],
            "b_rook": [(-3, 5, -2), (3, 2, -5)],
            "b_knight": [(-2, 5, -3), (2, 3, -5)],
            "b_bishop": [(0, 3, -3), (0, 4, -4), (0, 5, -5)],
            "b_queen": [(-1, 5, -4)],
            "b_king": [(1, 4, -5)],
        }

        initial_map = HexMap.from_radius(5)

        for key, pos_list in glinski_pos.items():
            for pos in pos_list:
                initial_map[HexCoord(*pos)] = key

        return initial_map

    def make_move(self, start, end):
        if start == end:
            return

        self[end] = self[start]
        self[start] = None

    def __iter__(self):
        return iter(self.cells.values())

    def __getitem__(self, item):
        return self.cells[item].state

    def __setitem__(self, key, value):
        self.cells[key].state = value

    def __contains__(self, item):
        return item in self.cells.keys()


class HexPixelAdapter:
    def __init__(self, dimensions, origin, hex_radius):
        self.dimensions = dimensions
        self.origin = origin
        self.hex_radius = hex_radius

    def hex_to_pixel(self, coord):
        x = self.hex_radius * 1.5 * coord.p + self.origin.x
        y = self.hex_radius * (math.sqrt(3) * 0.5 * coord.p + math.sqrt(3) * coord.r) + self.origin.y

        return PixelCoord(x, y)

    def pixel_to_hex(self, coord):
        coord -= self.origin

        p = 2 / 3 * coord.x / self.hex_radius
        r = (-1 / 3 * coord.x + math.sqrt(3) / 3 * coord.y) / self.hex_radius

        return HexCoord(p, -p - r, r)

    def get_vertices(self, coord):
        x, y = self.hex_to_pixel(coord)
        angle = math.pi / 3

        return [PixelCoord(
            self.hex_radius * math.cos(angle * i) + x,
            self.hex_radius * math.sin(angle * i) + y
        ) for i in range(6)]
