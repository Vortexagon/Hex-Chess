import math

from pixel import PixelCoord

move_vectors = {
    **dict.fromkeys(["w_bishop", "b_bishop"], [
        (2, -1, -1), (-2, 1, 1),
        (-1, 2, -1), (1, -2, 1),
        (-1, -1, 2), (1, 1, -2)
    ]),

    **dict.fromkeys(["w_rook", "b_rook"], [
        (0, 1, -1), (0, -1, 1),
        (1, 0, -1), (-1, 0, 1),
        (1, -1, 0), (-1, 1, 0)
    ]),

    **dict.fromkeys(["w_king", "b_king"], [
        (0, 1, -1), (0, -1, 1),
        (1, 0, -1), (-1, 0, 1),
        (1, -1, 0), (-1, 1, 0),
        (2, -1, -1), (-2, 1, 1),
        (-1, 2, -1), (1, -2, 1),
        (-1, -1, 2), (1, 1, -2)
    ]),

    **dict.fromkeys(["w_queen", "b_queen"], [
        (0, 1, -1), (0, -1, 1),
        (1, 0, -1), (-1, 0, 1),
        (1, -1, 0), (-1, 1, 0),
        (2, -1, -1), (-2, 1, 1),
        (-1, 2, -1), (1, -2, 1),
        (-1, -1, 2), (1, 1, -2)
    ]),

    **dict.fromkeys(["w_knight", "b_knight"], [
        (2, 1, -3), (3, -1, -2),
        (-1, 3, -2), (1, 2, -3),
        (-2, 3, -1), (-3, 2, 1),
        (-3, 1, 2), (-2, -1, 3),
        (-1, -2, 3), (1, -3, 2),
        (2, -3, 1), (3, -2, -1)
    ]),

    "w_pawn": [
        (0, 1, -1),
        (-1, 1, 0),
        (1, 0, -1)

    ],

    "b_pawn": [
        (0, -1, 1),
        (-1, 0, 1),
        (1, -1, 0)
    ]
}


class HexCoord:
    def __init__(self, p, q, r):
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
        return hash((self.p, self.q, self.r))

    def __abs__(self):
        return HexCoord(abs(self.p), abs(self.q), abs(self.r))

    def __iter__(self):
        return iter([self.p, self.q, self.r])


class HexCell:
    def __init__(self, coord, state=None):
        self.coord = coord
        self.state = state


class HexMap:
    def __init__(self, cells=None):
        if cells is None: cells = dict()
        self.cells = cells

    def __iter__(self):
        return iter(self.cells.values())

    def __getitem__(self, item):
        return self.cells[item].state

    def __setitem__(self, key, value):
        self.cells[key].state = value

    def __contains__(self, item):
        return item in self.cells.keys()

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

    def generate_moves(self, start: HexCoord):
        start_state = self[start]
        if start_state is None:
            return []

        valid_moves = [start]

        for ray in move_vectors[start_state]:
            ray = HexCoord(*ray)
            curr_hex = start

            while True:
                curr_hex += ray
                if curr_hex not in self:
                    break
                if self[curr_hex] is not None and self[curr_hex][0] == start_state[0]:
                    break
                if self.is_king_checked_after_move(start_state[0], start, curr_hex):
                    if start_state[2:] in ["king", "pawn", "knight"]:
                        break
                    else:
                        continue
                if start_state.endswith("pawn"):
                    offset = curr_hex - start
                    if start_state[0] == "w":
                        if offset in [HexCoord(-1, 1, 0), HexCoord(1, 0, -1)] and self[curr_hex] is None:
                            break
                        if offset == HexCoord(0, 1, -1) and self[curr_hex] is not None:
                            break
                    elif start_state[0] == "b":
                        if offset in [HexCoord(-1, 0, 1), HexCoord(1, -1, 0)] and self[curr_hex] is None:
                            break
                        if offset == HexCoord(0, -1, 1) and self[curr_hex] is not None:
                            break

                valid_moves.append(curr_hex)

                if self[curr_hex] is not None:
                    break
                if start_state[2:] in ["king", "pawn", "knight"]:
                    break

        return valid_moves

    def cells_with_state_col(self, color):
        valid_cells = []
        for cell in self:
            if cell.state is not None and cell.state.startswith(color):
                valid_cells.append(cell)
        return valid_cells

    def make_move(self, start, end):
        if start == end:
            return

        self[end] = self[start]
        self[start] = None

    def is_king_checked(self, color):
        king_coords = None
        for cell in self:
            if cell.state == f"{color}_king":
                king_coords = cell.coord

        for coord, cell in self.cells.items():
            if cell.state is None:
                continue
            if cell.state[0] == color:
                continue
            for ray in move_vectors[cell.state]:
                ray = HexCoord(*ray)
                curr_hex = cell.coord

                while True:
                    curr_hex += ray

                    if curr_hex not in self:
                        break
                    if self[curr_hex] is not None and self[curr_hex][0] == cell.state[0]:
                        break
                    if cell.state.endswith("pawn"):
                        offset = curr_hex - cell.coord
                        if cell.state[0] == "w":
                            if offset not in [HexCoord(-1, 1, 0), HexCoord(1, 0, -1)]:
                                break
                        elif cell.state[0] == "b":
                            if offset not in (HexCoord(-1, 0, 1), HexCoord(1, -1, 0)):
                                break
                    if curr_hex == king_coords:
                        return True
                    elif self[curr_hex] is not None:
                        break
                    elif cell.state[2:] in ["king", "pawn", "knight"]:
                        break
        return False

    def is_king_checked_after_move(self, color, start, end):
        prev_state = self[end]
        self.make_move(start, end)
        result = self.is_king_checked(color)
        self.make_move(end, start)
        self[end] = prev_state
        return result


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
