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


def draw_hex(cell, fill=False):
    pygame.draw.polygon(SCREEN, (255, 0, 0), ADAPTER.get_vertices(cell.coord), 0 if fill else 2)
    pixel_offset = PixelCoord(HEX_RADIUS, HEX_RADIUS) / 2

    if cell.state:
        pixel_coords = ADAPTER.hex_to_pixel(cell.coord)
        SCREEN.blit(piece_imgs[cell.state], pixel_coords - pixel_offset)


hover_coords = PixelCoord(0, 0)
hover_hex = HexCoord(0, 0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            # code to implement piece movement
            pass
        if event.type == pygame.MOUSEMOTION:
            hover_coords = PixelCoord(*pygame.mouse.get_pos())
            hover_hex = round(ADAPTER.pixel_to_hex(hover_coords))

    SCREEN.fill((255, 255, 255))

    for cell in HEX_MAP:
        draw_hex(cell)

    if hover_hex in HEX_MAP.cells:
        draw_hex(HEX_MAP.cells[hover_hex], fill=True)

    pygame.display.update()
