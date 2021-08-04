import pygame

from hex import HexPixelAdapter, HexMap
from pixel import PixelCoord

pygame.init()

SIDE_FONT = pygame.font.SysFont('Arial', 30)

GAME_DIMENSIONS = PixelCoord(600, 600)
SIDE_DIMENSIONS = PixelCoord(400, 0)
GAME_WIDTH, GAME_HEIGHT = GAME_DIMENSIONS
GAME_ORIGIN = GAME_DIMENSIONS / 2

SCREEN = pygame.display.set_mode(GAME_DIMENSIONS + SIDE_DIMENSIONS)
HEX_MAP = HexMap.from_glinski()
HEX_RADIUS = 30
HEX_COLORS = [(209, 139, 70), (252, 210, 164), (230, 171, 111)]
ADAPTER = HexPixelAdapter(GAME_DIMENSIONS, GAME_ORIGIN, HEX_RADIUS)
PIECE_OFFSET = PixelCoord(HEX_RADIUS, HEX_RADIUS) / 2

piece_names = [f"{color}_{name}" for color in "wb" for name in ("pawn", "rook", "knight", "bishop", "king", "queen")]
piece_imgs = {
    piece_name: pygame.transform.scale(
        pygame.image.load(f"img/{piece_name}.png").convert_alpha(),
        (HEX_RADIUS, HEX_RADIUS)
    )
    for piece_name in piece_names
}


def draw_hex(coord, color, fill=False):
    pygame.draw.polygon(SCREEN, color, ADAPTER.get_vertices(coord), 0 if fill else 3)


def draw_piece(cell):
    if cell.state and cell.coord != start_hex:
        pixel_coords = ADAPTER.hex_to_pixel(cell.coord)
        SCREEN.blit(piece_imgs[cell.state], pixel_coords - PIECE_OFFSET)


start_hex = None
piece_held = None
valid_moves = None

king_state = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            clicked_pixel = PixelCoord(*pygame.mouse.get_pos())
            clicked_hex = round(ADAPTER.pixel_to_hex(clicked_pixel))

            if clicked_hex not in HEX_MAP:
                continue
            clicked_state = HEX_MAP[clicked_hex]

            if not piece_held:
                if clicked_state is None:
                    continue
                piece_held = clicked_state
                start_hex = clicked_hex
                valid_moves = HEX_MAP.generate_moves(start_hex)
            else:
                if clicked_hex in valid_moves:
                    HEX_MAP.make_move(start_hex, clicked_hex)
                    piece_held = start_hex = None

                    if HEX_MAP.is_king_checked('w'):
                        if HEX_MAP.is_king_checkmated('w'):
                            king_state = "White King Checkmated! Black Wins"
                        else:
                            king_state = "White King Checked!"
                    elif HEX_MAP.is_king_checked('b'):
                        if HEX_MAP.is_king_checkmated('b'):
                            king_state = "Black King Checkmated White Wins"
                        else:
                            king_state = "Black King Checked!"
                    else:
                        king_state = ""

    SCREEN.fill((255, 255, 255))
    pygame.draw.line(SCREEN, (100, 100, 100), (GAME_WIDTH, 0), GAME_DIMENSIONS)

    SCREEN.blit(SIDE_FONT.render(king_state, True, (0, 0, 0)), (GAME_WIDTH, 50))

    for cell in HEX_MAP:
        color = HEX_COLORS[(cell.coord.q - cell.coord.r) % 3]
        draw_hex(cell.coord, color, fill=True)

    if start_hex is not None:
        for coord in valid_moves:
            color = (255, 50, 50) if HEX_MAP[coord] else (50, 255, 50)
            draw_hex(coord, color, fill=True)

        draw_hex(start_hex, (50, 50, 255), fill=True)

    for cell in HEX_MAP:
        draw_piece(cell)
        draw_hex(cell.coord, (0, 0, 0))

    if piece_held:
        SCREEN.blit(piece_imgs[piece_held], pygame.mouse.get_pos())

    pygame.display.flip()
