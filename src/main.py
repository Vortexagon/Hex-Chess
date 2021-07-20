import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_hex(vertices):
    pygame.draw.polygon(screen, (255, 0, 0), vertices, 2)


running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            # code to implement piece movement
            pass

    pygame.display.update()
