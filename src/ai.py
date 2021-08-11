import math
from typing import Optional

from hex import HexMap, HexCoord

class AI:
    capture_values = {
        None: 0,

        "w_pawn": 10,
        "w_rook": 40,
        "w_king": 150,
        "w_bishop": 40,
        "w_knight": 40,
        "w_queen": 250,

        "b_pawn": -10,
        "b_rook": -40,
        "b_king": -150,
        "b_bishop": -40,
        "b_knight": -40,
        "b_queen": -250,
    }
    searched = 0

    @staticmethod
    def move(hex_map: HexMap) -> tuple[HexCoord, HexCoord]:
        """
        Makes a move on the board, as Black, by calling a minimax search.
        """
        AI.searched = 0
        best_score: float = -math.inf
        best_move: Optional[tuple] = None

        for (start, end) in hex_map.moves_for_col("b"):

            prev_state = hex_map[end]
            hex_map.make_move(start, end)
            result: float = AI.minimax(hex_map, 0, -math.inf, math.inf, False)
            hex_map.make_move(end, start)
            hex_map[end] = prev_state

            if result > best_score:
                best_score = result
                best_move = (start, end)

        hex_map.make_move(*best_move)
        print(AI.searched)
        return best_move

    @staticmethod
    def minimax(hex_map: HexMap, depth: int, alpha: int, beta: int, maximising: bool) -> float:
        AI.searched += 1
        """
        Performs a minimax search down to a hardcoded depth.
        Will handle optimisations and heuristics.
        """
        # Add a limit on how far down to search.
        if depth >= 0:
            return AI.evaluate(hex_map)

        # This will make the initial score:
        # -Infinity for the maximiser
        # Infinity for the minimiser
        final_score: float = math.inf * (-1) ** maximising

        def capture_score(move: tuple[HexCoord, HexCoord]) -> int:
            value = AI.capture_values[hex_map[move[1]]]
            if value:
                return value
            else:
                return AI.evaluate(hex_map)

        moves = hex_map.moves_for_col("b" if maximising else "w")
        moves = sorted(moves, key=capture_score, reverse=maximising)

        for (start, end) in moves:

            prev_state = hex_map[end]
            hex_map.make_move(start, end)
            result: float = AI.minimax(hex_map, depth + 1, alpha, beta, not maximising)
            hex_map.make_move(end, start)
            hex_map[end] = prev_state

            if maximising:
                final_score = max(result, final_score)
                alpha = max(alpha, result)
                if beta <= final_score:
                    break
            else:
                final_score = min(result, final_score)
                beta = min(alpha, result)
                if alpha >= final_score:
                    break

        return final_score

    @staticmethod
    def evaluate(hex_map: HexMap) -> float:
        sum_vals = lambda cell: AI.capture_values[cell.state]
        return -sum(map(sum_vals, hex_map.cells_with_state_col("w"))) - sum(map(sum_vals, hex_map.cells_with_state_col("b")))
