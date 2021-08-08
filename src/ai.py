import math
from typing import Optional

from hex import HexMap, HexCell


class AI:
    @staticmethod
    def move(hex_map: HexMap):
        values = {
            None: -1,
            "w_pawn": 1,
            "w_knight": 3,
            "w_rook": 4,
            "w_bishop": 4,
            "w_queen": 10,
            "w_king": 10
        }

        best_score: int = -math.inf
        best_move: Optional[tuple] = None

        for cell in hex_map.cells_with_state_col("b"):
            for coord in hex_map.generate_moves(cell.coord):
                if coord != cell.coord:
                    result = values[hex_map[coord]]

                    if result > best_score:
                        best_score = result
                        best_move = (cell.coord, coord)

        hex_map.make_move(*best_move)
        return best_move
