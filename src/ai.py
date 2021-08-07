from hex import HexMap, HexCell


class AI:
    @staticmethod
    def move(hex_map: HexMap):
        for cell in hex_map.cells_with_state_col("b"):
            for coord in hex_map.generate_moves(cell.coord):
                if coord != cell.coord:
                    if hex_map.make_move(cell.coord, coord):
                        return
