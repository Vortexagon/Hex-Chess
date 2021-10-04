from typing import Optional

import pygame

from ai import AI
from hex import HexPixelAdapter, HexMap, HexCoord, HexCell
from pixel import PixelCoord

pygame.init()

SIDE_FONT = pygame.font.SysFont('Courier New', 30)  # The font for the side GUI.

GAME_DIMENSIONS: PixelCoord = PixelCoord(600, 600)  # The dimensions of the main game.
SIDE_DIMENSIONS: PixelCoord = PixelCoord(400, 0)  # The extra dimension needed for the side GUI.
GAME_WIDTH, GAME_HEIGHT = GAME_DIMENSIONS  # The width and height of the main game.
GAME_ORIGIN: PixelCoord = GAME_DIMENSIONS / 2  # The origin, the center of the main game.

SCREEN = pygame.display.set_mode(GAME_DIMENSIONS + SIDE_DIMENSIONS)  # The game display.
HEX_MAP: HexMap = HexMap.from_glinski()  # The game map.
HEX_RADIUS: float = 30  # The radius of an individual hex on the screen, in pixels.
HEX_COLORS: list[tuple] = [(209, 139, 70), (252, 210, 164), (230, 171, 111)]  # A list of the three board colours.
ADAPTER: HexPixelAdapter = HexPixelAdapter(GAME_DIMENSIONS, GAME_ORIGIN, HEX_RADIUS)  # The HexPixelAdapter for the map.
PIECE_OFFSET: PixelCoord = PixelCoord(HEX_RADIUS, HEX_RADIUS) / 2  # The offset so pieces are centered when drawn.

# Generate every combination of piece names.
piece_names: list[str] = [f"{color}_{name}" for color in "wb" for name in ("pawn", "rook", "knight", "bishop", "king", "queen")]

# Create a dict mapping those names to their respective image / surface.
piece_imgs = {
    piece_name: pygame.transform.scale(
        pygame.image.load(f"img/{piece_name}.png").convert_alpha(),
        (HEX_RADIUS, HEX_RADIUS)
    )
    for piece_name in piece_names
}


def draw_hex(coord: HexCoord, color: tuple, fill=False):
    """Draws a hex to the screen."""
    pygame.draw.polygon(SCREEN, color, ADAPTER.get_vertices(coord), 0 if fill else 3)


def draw_piece(cell: HexCell):
    """Draws a piece to the screen."""
    if cell.state is not None:
        # Don't draw the piece if it's in a user move, or an AI move.
        if cell.coord == start_hex:
            return
        elif is_ai_sprite_moving and cell.coord == ai_end_hex:
            return
        pixel_coords: PixelCoord = ADAPTER.hex_to_pixel(cell.coord)
        SCREEN.blit(piece_imgs[cell.state], pixel_coords - PIECE_OFFSET)


def update_whose_turn():
    """Check the ply and thus determine whose side's turn it is."""
    global is_even_ply
    is_even_ply = HEX_MAP.ply % 2 == 0
    global whose_turn_str
    whose_turn_str = "Your (White's) Turn!" if is_even_ply else "Black is Thinking ..."


def write_text(text: str, coordinates: tuple[int, int, int]):
    """A wrapper method for writing text onto the screen."""
    SCREEN.blit(SIDE_FONT.render(text, True, (0, 0, 0)), coordinates)


start_hex: Optional[HexCoord] = None  # When a move is in progress, this stores the starting coord.
piece_held: Optional[HexCoord] = None  # This stores the state of the piece held.
valid_moves: Optional[list[HexCoord]] = None  # This stores the valid moves of the piece held.
is_even_ply: bool = True  # Whether the current game ply is even or not.
king_state_str: str = ""  # A messsage on the check state of either king.
whose_turn_str: str = ""  # A message on whose side's turn it is.

is_ai_sprite_moving: bool = False  # Whether the AI sprite is moving across the board.
ai_start_hex: Optional[HexCoord] = None  # The `HexCoord` of the start of the AI's move.
ai_end_hex: Optional[HexCoord] = None  # The `HexCoord` of the end of the AI's move.
ai_curr_pixel: Optional[PixelCoord] = None  # The `PixelCoord` of the sprites current position
ai_end_pixel: Optional[PixelCoord] = None  # The `PixelCoord` of the end of the AI's move, also the sprites end point.
ai_sprite_state: Optional[str] = None  # The state of the piece that the AI moved.

ai_needs_turn: bool = False

update_whose_turn()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            # Convert the clicked coordinates to HexMap coords.
            clicked_pixel: PixelCoord = PixelCoord(*pygame.mouse.get_pos())
            clicked_hex: HexCoord = round(ADAPTER.pixel_to_hex(clicked_pixel))

            # An out of bounds check.
            if clicked_hex not in HEX_MAP:
                continue

            # Get the state of where we clicked.
            clicked_state: Optional[str] = HEX_MAP[clicked_hex]

            # If we're not already holding a piece:
            if not piece_held:
                # If there is nothing to pick up, we can't do much further.
                if clicked_state is None:
                    continue

                # There is a piece there, so grab the colour of it.
                color: str = clicked_state[0]

                # Make sure the colours take it in turns to move.
                if not ((is_even_ply and color == "w") or (not is_even_ply and color == "b")):
                    continue

                piece_held = clicked_state
                start_hex = clicked_hex
                valid_moves = HEX_MAP.generate_moves(start_hex)

            # Otherwise, we clicked while already holding a piece.
            else:
                if clicked_hex in valid_moves:
                    HEX_MAP.make_move(start_hex, clicked_hex)
                    piece_held = start_hex = None
                    if HEX_MAP.ply % 2:
                        ai_needs_turn = True
                        # update_whose_turn()
                        # break

                    # Update the king check / checkmate status string.
                    if HEX_MAP.is_king_checked('w'):
                        if HEX_MAP.is_king_checkmated('w'):
                            king_state_str = "White King Checkmated! Black Wins"
                        else:
                            king_state_str = "White King Checked!"
                    elif HEX_MAP.is_king_checked('b'):
                        if HEX_MAP.is_king_checkmated('b'):
                            king_state_str = "Black King Checkmated White Wins"
                        else:
                            king_state_str = "Black King Checked!"
                    else:
                        king_state_str = ""
                    update_whose_turn()

    SCREEN.fill((255, 255, 255))
    pygame.draw.line(SCREEN, (100, 100, 100), (GAME_WIDTH, 0), (GAME_WIDTH, GAME_HEIGHT))

    write_text(whose_turn_str, (GAME_WIDTH, 25))
    write_text(king_state_str, (GAME_WIDTH, 50))

    # Draw the light brown, brown and dark brown hexagons first.
    for cell in HEX_MAP:
        color: tuple[int, int, int] = HEX_COLORS[(cell.coord.q - cell.coord.r) % 3]
        draw_hex(cell.coord, color, fill=True)

    # Draw the valid moves for the current piece. Green = move, red = capture, blue = starting hex.
    if start_hex is not None:
        for coord in valid_moves:
            color: tuple[int, int, int] = (255, 50, 50) if HEX_MAP[coord] else (50, 255, 50)
            draw_hex(coord, color, fill=True)

        draw_hex(start_hex, (50, 50, 255), fill=True)

    # Color the cell that the AI just moved from, red.
    # Makes it easier to see what move the AI made.
    if ai_start_hex is not None:
        draw_hex(ai_start_hex, (200, 100, 100), fill=True)

    # Draw the pieces, and then the black wireframe.
    for cell in HEX_MAP:
        draw_piece(cell)
        draw_hex(cell.coord, (0, 0, 0))

    # If we're holding a piece, hover it under our mouse.
    if piece_held:
        SCREEN.blit(piece_imgs[piece_held], pygame.mouse.get_pos())

    # If the AI sprite is moving across the screen
    if is_ai_sprite_moving:
        SCREEN.blit(piece_imgs[ai_sprite_state], ai_curr_pixel)
        offset = ai_end_pixel - ai_curr_pixel

        # Move the piece's position a fifth closer to the end.
        ai_curr_pixel += offset * 0.2

        # If this isn't added, the piece would keep moving smaller and smaller amounts.
        # Moving would never finish.
        # So there's a minimum distance from which we say the move has now finished.
        if offset.mag() < 1:
            is_ai_sprite_moving = False

    pygame.display.flip()

    if ai_needs_turn:
        ai_start_hex, ai_end_hex = AI.move(HEX_MAP)
        update_whose_turn()
        is_ai_sprite_moving = True
        ai_curr_pixel = ADAPTER.hex_to_pixel(ai_start_hex) - PIECE_OFFSET
        ai_end_pixel = ADAPTER.hex_to_pixel(ai_end_hex) - PIECE_OFFSET
        ai_sprite_state = HEX_MAP[ai_end_hex]
        ai_needs_turn = False
