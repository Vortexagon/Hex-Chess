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
    cache = dict()

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
            result: float = AI.minimax(hex_map, 4, -math.inf, math.inf, False)
            hex_map.make_move(end, start)
            hex_map[end] = prev_state

            if result > best_score:
                best_score = result
                best_move = (start, end)

        hex_map.make_move(*best_move)
        return best_move

    @staticmethod
    def minimax(hex_map: HexMap, depth: int, alpha: float, beta: float, maximising: bool) -> float:
        """
        Performs a minimax search down to a variable depth.
        Will handle optimisations and heuristics.
        """
        state_hash = hash(hex_map.__str__())
        if state_hash in AI.cache:
            return AI.cache[state_hash]

        # Add a limit on how far down to search.
        if depth == 0:
            return AI.evaluate(hex_map)

        # This will make the initial score:
        # -Infinity for the maximiser
        # Infinity for the minimiser
        final_score: float = math.inf * (-1) ** maximising

        def capture_score(move: tuple[HexCoord, HexCoord]) -> int:
            return AI.capture_values[hex_map[move[0]]] + AI.capture_values[hex_map[move[1]]]

        moves = hex_map.moves_for_col("b" if maximising else "w")
        # moves = sorted(moves, key=capture_score, reverse=maximising)

        for (start, end) in moves:

            prev_state = hex_map[end]
            hex_map.make_move(start, end)
            result: float = AI.minimax(hex_map, depth - 1, alpha, beta, not maximising)
            hex_map.make_move(end, start)
            hex_map[end] = prev_state

            if maximising:
                final_score = max(result, final_score)
            else:
                alpha = max(alpha, result)
                final_score = min(result, final_score)
                beta = min(beta, result)

            if alpha <= beta:
                break

        AI.cache[state_hash] = final_score
        return final_score

    @staticmethod
    def evaluate(hex_map: HexMap) -> float:
        map_to_vals = lambda cell: AI.capture_values[cell.state]
        sum_vals = lambda col: sum(map(map_to_vals, hex_map.cells_with_state_col(col)))
        modifier: int = 0

        if hex_map.is_king_checked("w"):
            if hex_map.is_king_checkmated("w"):
                modifier = 1000
            else:
                modifier = 500
        elif hex_map.is_king_checked("b"):
            if hex_map.is_king_checkmated("b"):
                modifier = -1000
            else:
                modifier = -500

        return -(sum_vals("b") + sum_vals("w")) + modifier
