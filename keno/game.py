from time import sleep

import pygame

from keno import engine, BLACK, RED
from keno.controls import Button, Text, Image
from keno.boards import TileBoard, RewardsBoard


class Game:
    def __init__(self, screen, starting_money):
        self.screen = screen
        self.money = starting_money
        self.bet = 1

        self.background_image = pygame.image.load(r"assets\game_bg.jpg")

        self.button_menu = Button(screen, 1024-50, 0, 50, 25, "Menu", BLACK)

        self.image_title = Image(screen, 250, 35, r"assets\title.png")

        self.tile_board = TileBoard(screen, 100, 175)
        self.tile_unselected = pygame.image.load(r"assets\tiles_round\black.png")
        self.tile_selected = pygame.image.load(r"assets\tiles_round\blue.png")
        self.tile_hit = pygame.image.load(r"assets\tiles_round\red.png")
        self.tile_picked = pygame.image.load(r"assets\tiles_round\green.png")
        self.tile_board.load_images(self.tile_unselected, self.tile_selected, self.tile_hit, self.tile_picked)

        self.reward_board = RewardsBoard(screen, self.tile_board.right + 50, self.tile_board.top, self.tile_board, 22)

        self.button_play = Button(screen, self.tile_board.left, self.tile_board.bottom + 15, 100, 40, "Play")
        self.button_auto = Button(screen, self.button_play.right + 10, self.tile_board.bottom + 15, 100, 40, "Auto-Pick")
        self.button_clear = Button(screen, self.button_auto.right + 10, self.tile_board.bottom + 15, 100, 40, "Clear")

        self.button_bet_up = Button(screen, self.tile_board.left, self.button_play.bottom + 20, 60, 40, "Up")
        self.button_bet = Button(screen, self.button_bet_up.right + 10, self.button_play.bottom + 20, 60, 40, str(self.bet), BLACK)
        self.button_bet_down = Button(screen, self.button_bet.right + 10, self.button_play.bottom + 20, 60, 40, "Down")

        self.txt_money = Text(screen, self.button_clear.right + 40, self.button_clear.top, f"Money: ${self.money}")
        self.txt_payout = Text(screen, self.tile_board.right + 50, self.tile_board.bottom - self.tile_board.tile_size, "Won: $0")

    def run(self):
        clock = pygame.time.Clock()
        done = False
        while not done:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()

                    if self.button_menu.activated(pos):
                        done = True

                    self.tile_board.process_click(pos)

                    if self.button_play.activated(pos):
                        self.tile_board.clear_picks()
                        if len(self.tile_board._selected_tiles) > 0:
                            self.money -= self.bet
                            self.play(self.tile_board)
                            self.payout = engine.get_payout(len(self.tile_board.selected_tiles), len(self.tile_board.hit_tiles), self.bet)
                            self.money += self.payout
                            self.txt_payout.msg = f"Won: ${self.payout}"
                            if self.bet > self.money:
                                self.bet = self.money
                            if self.money < 1:
                                self.txt_money.color = RED
                                self.button_play.disable()
                                self.button_clear.disable()
                                self.button_auto.disable()
                                self.tile_board.disable()

                    if self.button_auto.activated(pos):
                        picks_needed = self.tile_board.max_selection - len(self.tile_board.selected_tiles)
                        new_picks = engine.get_random_list(picks_needed)
                        for pick in new_picks:
                            self.tile_board.mark_tile_selected(pick)

                    if self.button_clear.activated(pos):
                        self.tile_board.clear_all()

                    if self.button_bet_up.activated(pos):
                        if self.bet < 5 and self.money > self.bet:
                            self.bet += 1

                    if self.button_bet_down.activated(pos):
                        if self.bet > 1:
                            self.bet -= 1

            self.draw()

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0,0))
        self.button_menu.draw()
        self.image_title.draw()

        self.tile_board.draw_tiles()
        self.reward_board.update()
        self.reward_board.draw()

        self.button_play.draw()
        self.button_auto.draw()
        self.button_clear.draw()

        self.button_bet_up.draw()
        self.button_bet.msg = str(self.bet)
        self.button_bet.draw()
        self.button_bet_down.draw()
        self.txt_money.msg = f"Money: {self.money}"
        self.txt_money.draw()
        self.txt_payout.draw()

        pygame.display.update()

    def play(self, board):
        picks = engine.get_random_list(20)
        selections = board.selected_tiles
        board.draw_tiles()
        for pick in picks:
            sleep(.25)
            if pick in selections:
                board.mark_tile_hit(pick)
            else:
                board.mark_tile_picked(pick)
            board.draw_tile(pick)
            pygame.display.update()

class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.image_title = Image(self.screen, 250, 35, r"assets\title.png")
        self.button_game = Button(self.screen, 100, 175, 200, 50, "New Game")
        self.button_quit = Button(self.screen, self.button_game.left, self.button_game.bottom + 10, 200, 50, "Quit")
        self.background_image = pygame.image.load(r"assets\menu_bg.jpg")

    def run(self):
        clock = pygame.time.Clock()
        done = False

        while not done:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()

                    if self.button_game.activated(pos):
                        game = Game(self.screen, 35)
                        game.run()
                    elif self.button_quit.activated(pos):
                        done = True
            self.draw()

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0,0))
        self.image_title.draw()
        self.button_game.draw()
        self.button_quit.draw()

        pygame.display.update()

if __name__ == "__main__":

    menu = Menu()
    menu.run()