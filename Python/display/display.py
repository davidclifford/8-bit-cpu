import pygame
import random

WHITE = (255, 255, 255)


def main():
    pygame.init()
    size = (160, 160)
    screen = pygame.display.set_mode(size)
    quitit = False

    while quitit is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))

        # x = random.randint(0, 16*8-1)
        # y = random.randint(0, 15)
        for y in range(0, 15):
            for x in range(0, 16*8-1):
                pygame.draw.line(screen, WHITE, [x, y], [x, y])

        pygame.display.flip()

        for y in range(0, 15):
            for x in range(0, 16 * 8 - 1):
                pygame.draw.line(screen, (0,0,0), [x, y], [x, y])

        pygame.display.flip()

main()