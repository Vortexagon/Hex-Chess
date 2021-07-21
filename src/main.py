import pygame

from hex import HexPixelAdapter, HexMap

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
HEX_MAP = HexMap.from_radius(4)
ADAPTER = HexPixelAdapter((WIDTH, HEIGHT), (WIDTH / 2, HEIGHT / 2), 30)


def draw_hex(coord, fill=False):
    pygame.draw.polygon(SCREEN, (255, 0, 0), ADAPTER.get_vertices(coord), 0 if fill else 2)


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
