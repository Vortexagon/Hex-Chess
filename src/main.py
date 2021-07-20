import pygame

from hex import HexPixelAdapter, HexMap

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

HEX_MAP = HexMap.from_radius(4)
ADAPTER = HexPixelAdapter((WIDTH, HEIGHT), (WIDTH / 2, HEIGHT / 2), 30)


def draw_hex(coord):
    pygame.draw.polygon(SCREEN, (255, 0, 0), ADAPTER.get_vertices(coord), 2)


running = True
while running:
    SCREEN.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # code to implement piece movement
            pass

    for cell in HEX_MAP.cells.values():
        draw_hex(cell.coord)
    pygame.display.update()
