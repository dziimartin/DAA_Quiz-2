import pygame
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.mode = None 
        self.playing = False

    def new(self):
        self.board = Board()
        self.board.display_board()
        self.win = False
        self.playing = True

        clue_count = {"easy": 20, "medium": 10, "hard": 3}.get(self.mode, 3)

        c_tiles = [
            (x, y) for x, row in enumerate(self.board.board_list)
            for y, tile in enumerate(row) if tile.type == "C"
        ]
        random.shuffle(c_tiles)
        for i in range(min(clue_count, len(c_tiles))):
            x, y = c_tiles[i]
            self.board.board_list[x][y].revealed = True

    def run(self):
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if event.button == 1:
                    if not self.board.board_list[mx][my].flagged:
                        if not self.board.dig(mx, my):
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "X":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == "X":
                                        tile.revealed = True
                            self.state = "lose"
                            self.playing = False

                if event.button == 3:
                    if not self.board.board_list[mx][my].revealed:
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged

                if self.check_win():
                    self.win = True
                    self.playing = False
                    self.state = "win"
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True

    def menu_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.draw_text("MINESWEEPER", 48, WIDTH // 2, HEIGHT // 6)

            easy_btn = self.draw_text("Easy", 30, WIDTH // 2, HEIGHT // 3, bg=(50, 100, 50))
            medium_btn = self.draw_text("Medium", 30, WIDTH // 2, HEIGHT // 2, bg=(100, 100, 50))
            hard_btn = self.draw_text("Hard", 30, WIDTH // 2, HEIGHT // 1.5, bg=(100, 50, 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_btn.collidepoint(event.pos):
                        self.mode = "easy"
                        self.state = "playing"
                        return
                    elif medium_btn.collidepoint(event.pos):
                        self.mode = "medium"
                        self.state = "playing"
                        return
                    elif hard_btn.collidepoint(event.pos):
                        self.mode = "hard"
                        self.state = "playing"
                        return

    def win_screen(self):
        while True:
            self.screen.fill((0, 100, 0))
            self.draw_text("YOU WIN!", 48, WIDTH // 2, HEIGHT // 4)

            restart_btn = self.draw_text("Restart", 30, WIDTH // 2, HEIGHT // 2, bg=(0, 150, 0))
            menu_btn = self.draw_text("Main Menu", 30, WIDTH // 2, HEIGHT // 1.5, bg=(0, 80, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.collidepoint(event.pos):
                        self.state = "playing"
                        return
                    elif menu_btn.collidepoint(event.pos):
                        self.state = "menu"
                        return

    def lose_screen(self):
        while True:
            self.screen.fill((100, 0, 0))
            self.draw_text("GAME OVER", 48, WIDTH // 2, HEIGHT // 4)

            restart_btn = self.draw_text("Restart", 30, WIDTH // 2, HEIGHT // 2, bg=(150, 0, 0))
            menu_btn = self.draw_text("Main Menu", 30, WIDTH // 2, HEIGHT // 1.5, bg=(80, 0, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.collidepoint(event.pos):
                        self.state = "playing"
                        return
                    elif menu_btn.collidepoint(event.pos):
                        self.state = "menu"
                        return

    def draw_text(self, text, size, x, y, color=(255, 255, 255), bg=None, padding=10):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))

        if bg:
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(self.screen, bg, bg_rect, border_radius=8)
            self.screen.blit(text_surface, text_rect)
            return bg_rect
        else:
            self.screen.blit(text_surface, text_rect)
            return text_rect

game = Game()
while True:
    if game.state == "menu":
        game.menu_screen()
    elif game.state == "playing":
        game.new()
        game.run()
    elif game.state == "win":
        game.win_screen()
    elif game.state == "lose":
        game.lose_screen()