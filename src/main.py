import pygame

from hex import HexPixelAdapter, HexMap

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HEX_MAP = HexMap.from_radius(4)
HEX_RADIUS = 30
ADAPTER = HexPixelAdapter((WIDTH, HEIGHT), (WIDTH / 2, HEIGHT / 2), HEX_RADIUS)

piece_names = [f"{color}_{name}" for color in "wb" for name in ("pawn", "rook", "knight", "bishop", "king", "queen")]
piece_imgs = {
    piece_name: pygame.transform.scale(
        pygame.image.load(f"img/{piece_name}.png").convert_alpha(),
        (HEX_RADIUS, HEX_RADIUS)
    )
    for piece_name in piece_names
}


def draw_hex(coord, fill=False):
    pygame.draw.polygon(SCREEN, (255, 0, 0), ADAPTER.get_vertices(coord), 0 if fill else 2)

    pixel_coords = ADAPTER.hex_to_pixel(coord)

    SCREEN.blit(piece_imgs["w_pawn"], (pixel_coords[0] - HEX_RADIUS / 2, pixel_coords[1] - HEX_RADIUS / 2))


hover_coords = (0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            # code to implement piece movement
            pass
        if event.type == pygame.MOUSEMOTION:
            hover_coords = pygame.mouse.get_pos()

    SCREEN.fill((255, 255, 255))

    for cell in HEX_MAP:
        draw_hex(cell.coord)
    draw_hex(round(ADAPTER.pixel_to_hex(hover_coords)), fill=True)

    pygame.display.update()
