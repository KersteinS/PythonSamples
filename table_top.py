"""show my table top"""

from math import ceil, floor
import pygame
import pygame.locals as pgl
from pygame.rect import Rect
from pygame.surface import Surface

# (width,height)
# front of a card has number (or face) and suit, back is the deck art (red or blue)
# 13 cards with 3 face card slots is max per caravan
# 2,2 is red discard; 3,2 is red draw; 4,2 is blue draw; 5,2 is blue discard [3:4][9:11] are the caravan slots

class CardSprite(pygame.sprite.Sprite):
    """Test sprite for a card"""
    def __init__(self, color: Surface, card: Surface, location: list) -> None:
        super().__init__()
        self.back = color
        self.front = card
        self.image = self.back# self.image is a Surface in every case
        #self.image = self.back.subsurface((5, 5, 108, 160))# this is image without outline if color or card have outline
        self.rect = Rect(location[0]+10, location[1]+10, 128, 180)

    def set_front(self):
        self.image = self.front
        return self
    def set_back(self):
        self.image = self.back
        return self

class OutlineSprite(pygame.sprite.Sprite):
    """Test sprite for an outline"""
    def __init__(self, outline: Surface, location: list) -> None:
        super().__init__()
        self.image = outline# self.image is a Surface in every case
        self.rect = Rect(location[0]+5, location[1]+5, 128, 180)

def simple_to_two_d(index: int) -> tuple:
    """convert the index of the item in simple_grid to a row and col for grid"""
    col = index-(floor(index/15)*15)
    return ceil(index/15), col if col else 15

def two_d_to_simple(row: int, col: int):
    """convert grid row and col to index for item in simple_grid"""
    return ((row-1)*15)+col

def access_two_d(_list:list, xy:tuple):
    """given a 2D _list and a tuple (x,y) find the value at _list[x][y]"""
    return _list [xy[0]] [xy[1]]

def find_click_rect(location:tuple[int, int]) -> tuple:
    """given pixel location of a click, find the rect in grid that has been clicked"""
    x,y = location
    row = ceil(y/180)
    col = ceil(x/128)
    return row if row else 1, col if col else 1

def place_card(screen, card, location:list, highlight: bool, outline):
    """given a row and col, place the desired card there. UNUSED"""
    rects = []
    x = location[0] + 10
    y = location[1] + 10
    rects.append(screen.blit(card, (x,y)))
    if highlight:
        x = location[0] + 5
        y = location[1] + 5
        rects.append(screen.blit(outline, (x,y)))
    return rects

def draw(screen, table_top, values, grid, red_card, blue_card, outline):
    """every loop redraw everything. UNUSED"""
    rects = []
    for index, value in enumerate(values):
        row, col = simple_to_two_d(index+1)# +1 to account for simple_grid being 0 indexed
        if value["draw"]:
            if row < 4:
                rects.extend(place_card(screen, red_card, grid[row][col], value["outline"], outline))
            else:
                rects.extend(place_card(screen, blue_card, grid[row][col], value["outline"], outline))
        else:
            x,y = grid[row][col]
            rects.append(screen.blit(table_top, (x,y), (x,y, 128,180)))
    return rects

def main():
    """main function"""
    pygame.init()
    display_info = pygame.display.Info()
    screen = pygame.display.set_mode((display_info.current_w, display_info.current_h-50))
    screen.set_alpha(None)# performance mod
    pygame.event.set_allowed([pgl.QUIT, pgl.MOUSEBUTTONDOWN, pgl.MOUSEMOTION, pgl.MOUSEBUTTONUP])# performance mod
    table_top = pygame.image.load(".\\art\\TableTop.jpg").convert()
    red_card = pygame.image.load(".\\art\\red_card_back.jpg").convert()
    blue_card = pygame.image.load(".\\art\\blue_card_back.jpg").convert()
    front_face = pygame.image.load(".\\art\\front_face.jpg").convert()
    y_outline = pygame.image.load(".\\art\\outline_y.png").convert()
    y_outline.set_colorkey((255,255,255))# makes it so the white in the image is not blitted (drawn)
    g_outline = pygame.image.load(".\\art\\outline_g.png").convert()
    g_outline.set_colorkey((255,255,255))# makes it so the white in the image is not blitted (drawn)
    grid = [[]]
    for i in range(6):
        b = [[]]
        for j in range(15):
            b.append([128*j,180*i])
        grid.append(b)
    # grid is 6x15 (ROWxCOL) containing the coords of the upper left corner
    # of the 128x180 pixel rect correllating to that location on a 1920x1080 display
    # grid is NOT 0 indexed, simple_grid IS 0 indexed
    background = pygame.sprite.Sprite()
    background.image = table_top
    background.rect = Rect(0,0, 1920, 1080)
    cards = [CardSprite(red_card, front_face, access_two_d(grid, simple_to_two_d(i))) for i in range(1,46)]
    cards.extend([CardSprite(blue_card, front_face, access_two_d(grid, simple_to_two_d(i))) for i in range(46,91)])
    y_outlines = [OutlineSprite(y_outline, access_two_d(grid, simple_to_two_d(i))) for i in range(1,46)]
    y_outlines.extend([OutlineSprite(y_outline, access_two_d(grid, simple_to_two_d(i))) for i in range(46,91)])
    g_outlines = [OutlineSprite(g_outline, access_two_d(grid, simple_to_two_d(i))) for i in range(1,46)]
    g_outlines.extend([OutlineSprite(g_outline, access_two_d(grid, simple_to_two_d(i))) for i in range(46,91)])
    abc = [
        {
        "display_value": list(range(7)),
        "back": cards[i].set_back,
        "front": cards[i].set_front,
        "0":[cards[i], y_outlines[i], g_outlines[i]],
        "1": [cards[i]],
        "2": [cards[i], y_outlines[i]],
        "3":[cards[i], g_outlines[i]],
        "4":[cards[i]],
        "5": [cards[i], y_outlines[i]],
        "6":[cards[i], g_outlines[i]],
        }
        for i in range(90)
    ]
    del cards, y_outlines, g_outlines
    active_group = pygame.sprite.RenderUpdates(background)
    hovered_group = pygame.sprite.RenderUpdates()
    dragging_group = pygame.sprite.RenderUpdates()
    run = True
    while run:
        updated_rects = []
        current_mouse_pos = pygame.mouse.get_pos()

        # show highlight sprite for hovered grid location
        hovered_group.empty()
        if pygame.mouse.get_focused():
            row, col = find_click_rect(current_mouse_pos)
            index = two_d_to_simple(row, col) - 1# -1 to account for simple_grid being 0 indexed
            if abc[index]["display_value"][0] == 0:
                hovered_group.add(abc[index]["3"][1])

        # process events
        for event in pygame.event.get():
            if event.type == pgl.QUIT:
                run = False
                break

            elif event.type == pgl.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                row, col = find_click_rect(event.pos)
                index = two_d_to_simple(row, col) - 1# -1 to account for simple_grid being 0 indexed
                sprite_set = abc[index]
                if left:# process left clicks
                    if sprite_set["display_value"][0] != 0:
                        start_pos = grid[row][col]
                        dragging_group.add(abc[index][str(abc[index]["display_value"][0])])
                if right:# process right clicks
                    sprite_set["display_value"] = list(range(7))

            elif event.type == pgl.MOUSEMOTION and len(dragging_group):
                mouse_pos = event.pos
                for sprite in dragging_group.sprites()[::-1]:
                    end_pos = access_two_d(grid,find_click_rect(mouse_pos))
                    if start_pos != end_pos:
                        if isinstance(sprite, CardSprite):
                            sprite.rect = Rect(end_pos[0]+10, end_pos[1]+10, 128, 180)
                        elif isinstance(sprite, OutlineSprite):
                            sprite.rect = Rect(end_pos[0]+5, end_pos[1]+5, 128, 180)
                        active_group.add(sprite)
                        break

            elif event.type == pgl.MOUSEBUTTONUP:
                print(left, middle, right)
                if len(dragging_group):
                    dragging_group.empty()
                    print("dragon")
                else:
                    row, col = find_click_rect(event.pos)
                    index = two_d_to_simple(row, col) - 1# -1 to account for simple_grid being 0 indexed
                    sprite_set = abc[index]
                    dv = sprite_set["display_value"][0]
                    if dv == 0:
                        sprite_set["front"]()
                    elif dv == 3:
                        active_group.remove(sprite_set["0"])
                        sprite_set["back"]()
                    sprite_set["display_value"].append(sprite_set["display_value"].pop(0))

        #remove or add sprites in active, then draw screen
        for sprite_set in abc:
            if sprite_set["display_value"][0] == 0:
                active_group.remove(sprite_set["0"])
            else:
                active_group.add(sprite_set[str(sprite_set["display_value"][0])])
        updated_rects.extend(active_group.draw(screen))
        updated_rects.extend(hovered_group.draw(screen))
        pygame.display.update(updated_rects)
    pygame.quit()

if __name__ == "__main__":
    main()
    print("Finished")