import math
from typing import Optional

from hex import HexMap, HexCoord


class AI:
    @staticmethod
    def move(hex_map: HexMap) -> tuple[HexCoord, HexCoord]:
        """
        Makes a move on the board, as Black, by calling a minimax search.
        """

        best_score: float = -math.inf
        best_move: Optional[tuple] = None

        for (start, end) in hex_map.moves_for_col("b"):

            prev_state = hex_map[end]
            hex_map.make_move(start, end)
            result: float = AI.minimax(hex_map, 0, False)
            hex_map.make_move(end, start)
            hex_map[end] = prev_state

            if result > best_score:
                best_score = result
                best_move = (start, end)

        hex_map.make_move(*best_move)
        return best_move

    @staticmethod
    def minimax(hex_map: HexMap, depth: int, maximising: bool) -> float:
        """
        Performs a minimax search down to a hardcoded depth.
        Will handle optimisations and heuristics.
        """
        # Add a limit on how far down to search.
        if depth >= 1:
            return AI.evaluate(hex_map)

        # This will make the initial score:
        # -Infinity for the maximiser
        # Infinity for the minimiser
        final_score: float = math.inf * (-1) ** maximising

        for (start, end) in hex_map.moves_for_col("b" if maximising else "w"):

            prev_state = hex_map[end]
            hex_map.make_move(start, end)
            result: float = AI.minimax(hex_map, depth + 1, not maximising)
            hex_map.make_move(end, start)
            hex_map[end] = prev_state

            if maximising:
                final_score = max(result, final_score)
            else:
                final_score = min(result, final_score)

        return final_score

    @staticmethod
    def evaluate(hex_map: HexMap) -> float:
        return len(hex_map.cells_with_state_col("b")) - len(hex_map.cells_with_state_col("w"))
