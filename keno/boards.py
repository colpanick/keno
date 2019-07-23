import pygame
from keno.buttons import Tile
from keno import engine, RED, GREEN, BLUE, WHITE

class TileBoard():
    def __init__(self, screen, x, y, dimensions=(10, 8), max_selection=10, tile_size=50, tile_padding=5):
        self.screen = screen
        self.x = x
        self.y = y
        self.dimensions = dimensions
        self.max_selection = max_selection
        self.tile_size = tile_size
        self.tile_padding = tile_padding

        self.tiles = self.generate_tiles()
        self._selected_tiles = []
        self._picked_tiles = []
        self._hit_tiles = []

    @property
    def selected_tiles(self):
        return [tile.number for tile in self._selected_tiles]

    @property
    def picked_tiles(self):
        return [tile.number for tile in self._picked_tiles]

    @property
    def hit_tiles(self):
        return [tile.number for tile in self._hit_tiles]

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + (self.dimensions[0] * self.tile_size) + (self.dimensions[0] -1) * self.tile_padding

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + (self.dimensions[1] * self.tile_size) + (self.dimensions[1] - 1) * self.tile_padding

    def generate_tiles(self):
        tile_dict = {}

        tile_y = self.y
        curr_tile = 1
        for _ in range(self.dimensions[1]):
            tile_x = self.x
            for _ in range(self.dimensions[0]):
                tile_dict[curr_tile] = Tile(self.screen, tile_x, tile_y, self.tile_size, curr_tile)
                curr_tile += 1
                tile_x += self.tile_size + self.tile_padding
            tile_y += self.tile_size + self.tile_padding
        return tile_dict

    def draw_tiles(self):
        for _, tile in self.tiles.items():
            tile.draw()

    def mark_tile_selected(self, tile_num):
        if len(self._selected_tiles) < self.max_selection:
            tile = self.tiles[tile_num]
            tile.color = BLUE
            tile.bcolor = GREEN
            tile.tcolor = GREEN
            self._selected_tiles.append(tile)

    def mark_tile_unselected(self, tile_num):
        tile = self.tiles[tile_num]
        tile.color = BLUE
        tile.bcolor = WHITE
        tile.tcolor = WHITE
        try:
            self._selected_tiles.remove(tile)
        except ValueError:
            pass

    def mark_tile_picked(self, tile_num):
        tile = self.tiles[tile_num]
        tile.color = RED
        tile.bcolor = BLUE
        tile.tcolor = WHITE
        self._picked_tiles.append(tile)

    def mark_tile_hit(self, tile_num):
        tile = self.tiles[tile_num]
        tile.color = GREEN
        tile.bcolor = BLUE
        tile.tcolor = WHITE
        self._hit_tiles.append(tile)

    def clear_all(self):
        for tile in self.tiles:
            self.mark_tile_unselected(tile)
            self._selected_tiles = []
            self._picked_tiles = []
            self._hit_tiles = []

    def clear_picks(self):
        selected_tiles = self.selected_tiles
        self.clear_all()
        for tile in selected_tiles:
            self.mark_tile_selected(tile)

    def process_click(self, coords):
        self.clear_picks()
        for tile_num, tile in self.tiles.items():
            if tile.activated(coords):
                if tile in self._selected_tiles:
                    self.mark_tile_unselected(tile_num)
                else:
                    self.mark_tile_selected(tile_num)

    def disable(self):
        for _, tile in self.tiles.items():
            tile.disable()

    def enable(self):
        for _, tile in self.tiles.items():
            tile.enable()

class RewardsBoard:
    def __init__(self, screen, x, y, tile_board, font_size):
        self.screen = screen
        self.x = x
        self.y = y
        self.board = tile_board
        self.font_size = font_size

        self.update()

    def update(self):

        current_selections = len(self.board.selected_tiles)
        self.rewards = engine.get_payout_list(current_selections)

    def draw(self):
        if self.board.hit_tiles or self.board.picked_tiles:
            show_reward_hit = True
        else:
            show_reward_hit = False

        y_modifier = 0
        for hits, reward in self.rewards.items():
            if show_reward_hit and int(hits) == len(self.board.hit_tiles):
                font_color = GREEN
            else:
                font_color = WHITE
            font = pygame.font.SysFont("comicsansms", self.font_size)
            hits_text = font.render(hits, True, font_color)
            reward_text = font.render(reward, True, font_color)
            text_h = hits_text.get_rect()[3]

            self.screen.blit(hits_text,(self.x, self.y + y_modifier, 50, text_h))
            self.screen.blit(reward_text,(self.x + 50, self.y + y_modifier, 50, text_h))
            y_modifier += text_h
