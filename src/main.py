import pygame

from hex import HexPixelAdapter, HexMap, HexCoord
from pixel import PixelCoord

pygame.init()

DIMENSIONS = PixelCoord(800, 600)
WIDTH, HEIGHT = DIMENSIONS
ORIGIN = DIMENSIONS / 2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HEX_MAP = HexMap.from_glinski()
HEX_RADIUS = 30
ADAPTER = HexPixelAdapter(DIMENSIONS, ORIGIN, HEX_RADIUS)

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
    pixel_offset = PixelCoord(HEX_RADIUS, HEX_RADIUS) / 2

    if cell.state and cell.coord != start_hex:
        pixel_coords = ADAPTER.hex_to_pixel(cell.coord)
        SCREEN.blit(piece_imgs[cell.state], pixel_coords - pixel_offset)


hover_pixel = PixelCoord(0, 0)
hover_hex = HexCoord(0, 0, 0)

start_hex = None
piece_held = None

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
                piece_held = clicked_state
                start_hex = clicked_hex
            else:
                if HEX_MAP.validate_move(start_hex, clicked_hex):
                    HEX_MAP.make_move(start_hex, clicked_hex)
                    piece_held = start_hex = None

        if event.type == pygame.MOUSEMOTION:
            hover_pixel = PixelCoord(*pygame.mouse.get_pos())
            hover_hex = round(ADAPTER.pixel_to_hex(hover_pixel))

    SCREEN.fill((255, 255, 255))

    if hover_hex in HEX_MAP.cells:
        draw_hex(HEX_MAP.cells[hover_hex].coord, (200, 200, 200), fill=True)

    if start_hex is not None:
        for coord in HEX_MAP.generate_moves(start_hex):
            color = [(255, 0, 0), (0, 255, 0)][HEX_MAP[coord] is None]
            draw_hex(coord, color, fill=True)

    for cell in HEX_MAP:
        draw_piece(cell)

    for cell in HEX_MAP:
        draw_hex(cell.coord, (0, 0, 0))

    if piece_held:
        SCREEN.blit(piece_imgs[piece_held], pygame.mouse.get_pos())

    pygame.display.update()
