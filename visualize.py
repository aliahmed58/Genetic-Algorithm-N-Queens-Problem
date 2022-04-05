import pygame

pygame.font.init()
f = pygame.font.SysFont("Comic Sans MS", 20)

pygame.init()


def visualize_board(state):
    screen = pygame.display.set_mode((400, 400))
    screen.fill((255, 255, 255, 1))
    draw_grid(state, screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()


def draw_grid(state, screen):
    block_size = int(400 / len(state))
    count = 0
    screen.fill((255, 255, 255, 1))
    for x in range(0, 400, block_size):
        t = f'Q{count + 1}'
        t_s = f.render(t, False, (0, 0, 0))
        r = pygame.Rect(x, block_size * (state[count] - 1), block_size, block_size)
        pygame.draw.rect(screen, (0, 255, 0, 1), r, block_size)
        screen.blit(t_s, (x + 10, block_size * (state[count] - 1)))
        for z in range(0, 400, block_size):
            rect = pygame.Rect(x, z, block_size, block_size)
            pygame.draw.rect(screen, (0, 0, 0, 1), rect, 1)
        count += 1
