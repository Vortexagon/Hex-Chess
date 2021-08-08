import math
from typing import Optional

from hex import HexMap, HexCell


class AI:
    @staticmethod
    def move(hex_map: HexMap):

        best_score: float = -math.inf
        best_move: Optional[tuple] = None

        for cell in hex_map.cells_with_state_col("b"):
            for coord in hex_map.generate_moves(cell.coord):
                if coord != cell.coord:

                    prev_state = hex_map[coord]
                    hex_map.make_move(cell.coord, coord)
                    result = AI.minimax(hex_map, 0, False)
                    hex_map.make_move(coord, cell.coord)
                    hex_map[coord] = prev_state

                    if result > best_score:
                        best_score = result
                        best_move = (cell.coord, coord)

        hex_map.make_move(*best_move)
        return best_move

    @staticmethod
    def minimax(hex_map: HexMap, depth: int, maximising: bool) -> float:
        # Add a limit on how far down to search.
        if depth >= 1:
            return AI.evaluate(hex_map)

        # This will make the initial score:
        # -Infinity for the maximiser
        # Infinity for the minimiser
        final_score: float = math.inf * (-1) ** maximising

        for cell in hex_map.cells_with_state_col("b" if maximising else "w"):
            for coord in hex_map.generate_moves(cell.coord):
                if coord != cell.coord:

                    prev_state = hex_map[coord]
                    hex_map.make_move(cell.coord, coord)
                    result: float = AI.minimax(hex_map, depth + 1, not maximising)
                    hex_map.make_move(coord, cell.coord)
                    hex_map[coord] = prev_state

                    if maximising:
                        final_score = max(result, final_score)
                    else:
                        final_score = min(result, final_score)

        return final_score

    @staticmethod
    def evaluate(hex_map: HexMap) -> float:
        return 0
