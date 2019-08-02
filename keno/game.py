from time import sleep

import pygame

from keno import screen, clock, engine, BLACK, WHITE, BLUE, RED, GREEN
from keno.controls import Button, Text, Image
from keno.boards import TileBoard, RewardsBoard



def play(board):
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


def game(money):
    bet = 1

    background_image = pygame.image.load(r"assets\game_bg.jpg")

    button_menu = Button(screen, 1024-50, 0, 50, 25, "Menu", BLACK)

    image_title = Image(screen, 250, 35, r"assets\title.png")

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

    txt_money = Text(screen, button_clear.right + 40, button_clear.top, f"Money: ${money}")
    txt_payout = Text(screen, tile_board.right + 50, tile_board.bottom - tile_board.tile_size, "Won: $0")



    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if button_menu.activated(pos):
                    done = True

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
        button_menu.draw()
        image_title.draw()

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

def menu():
    image_title = Image(screen, 250, 35, r"assets\title.png")
    button_game = Button(screen, 100, 175, 200, 50, "New Game")
    button_quit = Button(screen, button_game.left, button_game.bottom + 10, 200, 50, "Quit")
    background_image = pygame.image.load(r"assets\menu_bg.jpg")

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if button_game.activated(pos):
                    game(30)
                elif button_quit.activated(pos):
                    done = True

        screen.fill(BLACK)
        screen.blit(background_image, (0,0))
        image_title.draw()
        button_game.draw()
        button_quit.draw()

        clock.tick(30)
        pygame.display.update()

if __name__ == "__main__":

    menu()