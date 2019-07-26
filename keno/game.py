import pygame

from keno import screen, clock, engine, BLACK, WHITE, BLUE, RED, GREEN
from keno.controls import Button
from keno.boards import TileBoard, RewardsBoard



class Text:
    def __init__(self, screen, x, y, w, h, msg, color=WHITE, size=22):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.msg = msg
        self.color = color
        self.size = size

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    def draw(self):
        font = pygame.font.SysFont("comicsansms", self.size)
        text = font.render(self.msg, True, self.color)
        self.screen.blit(text, (self.x,self.y,self.w,self.h))

def play(board):
    picks = engine.get_random_list(20)
    selections = board.selected_tiles

    for pick in picks:
        if pick in selections:
            board.mark_tile_hit(pick)
        else:
            board.mark_tile_picked(pick)

def game():
    money = 25
    bet = 1

    background_image = pygame.image.load(r"assets\game_bg.jpg")

    title_image = pygame.image.load(r"assets\title.png")
    title_coords = title_image.get_rect()
    title_coords.center = (1024/2, 75)

    tile_board = TileBoard(screen, 100, 175)
    tile_unselected = pygame.image.load(r"assets\tiles_round\black.png")
    tile_selected = pygame.image.load(r"assets\tiles_round\blue.png")
    tile_hit = pygame.image.load(r"assets\tiles_round\red.png")
    tile_picked = pygame.image.load(r"assets\tiles_round\green.png")
    tile_board.load_images(tile_unselected, tile_selected, tile_hit, tile_picked)

    reward_board = RewardsBoard(screen, tile_board.right + 50, tile_board.top, tile_board, 22)

    button_play = Button(screen, tile_board.left, tile_board.bottom + 15, 100, 40, "Play")
    button_auto = Button(screen, button_play.right + 10, tile_board.bottom + 15, 100, 40, "Auto-Pick")
    button_clear = Button(screen, button_auto.right + 10, tile_board.bottom + 15, 100, 40, "Clear")

    button_bet_up = Button(screen, tile_board.left, button_play.bottom + 20, 60, 40, "Up")
    button_bet = Button(screen, button_bet_up.right + 10, button_play.bottom + 20, 60, 40, str(bet), BLACK)
    button_bet_down = Button(screen, button_bet.right + 10, button_play.bottom + 20, 60, 40, "Down")

    txt_money = Text(screen, button_clear.right + 40, button_clear.top, 150, 25, f"Money: ${money}")
    txt_payout = Text(screen, tile_board.right + 50, tile_board.bottom - tile_board.tile_size, 150, 22, "Won: $0")



    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                tile_board.process_click(pos)

                if button_play.activated(pos):
                    tile_board.clear_picks()
                    if len(tile_board._selected_tiles) > 0:
                        money -= bet
                        play(tile_board)
                        payout = engine.get_payout(len(tile_board.selected_tiles), len(tile_board.hit_tiles), bet)
                        money += payout
                        txt_payout.msg = f"Won: ${payout}"
                        if bet > money:
                            bet = money
                        if money < 1:
                            txt_money.color = RED
                            button_play.disable()
                            button_clear.disable()
                            button_auto.disable()
                            tile_board.disable()

                if button_auto.activated(pos):
                    picks_needed = tile_board.max_selection - len(tile_board.selected_tiles)
                    new_picks = engine.get_random_list(picks_needed)
                    for pick in new_picks:
                        tile_board.mark_tile_selected(pick)

                if button_clear.activated(pos):
                    tile_board.clear_all()

                if button_bet_up.activated(pos):
                    if bet < 5 and money > bet:
                        bet += 1

                if button_bet_down.activated(pos):
                    if bet > 1:
                        bet -= 1

        screen.fill(BLACK)
        screen.blit(background_image, (0,0))
        screen.blit(title_image, (title_coords))

        tile_board.draw_tiles()
        reward_board.update()
        reward_board.draw()

        button_play.draw()
        button_auto.draw()
        button_clear.draw()

        button_bet_up.draw()
        button_bet.msg = str(bet)
        button_bet.draw()
        button_bet_down.draw()
        txt_money.msg = f"Money: {money}"
        txt_money.draw()
        txt_payout.draw()

        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":

    game()