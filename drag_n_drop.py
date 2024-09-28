from math import ceil, floor
import pygame
import pygame.locals as pgl
from pygame.rect import Rect
from pygame.surface import Surface

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
    my_card = CardSprite(blue_card, front_face, grid[4][10])
    my_card2 = CardSprite(red_card, front_face, grid[4][11])
    background_group = pygame.sprite.RenderUpdates(background)
    active_group = pygame.sprite.RenderUpdates([my_card, my_card2])
    moving_group = pygame.sprite.RenderUpdates()
    run = True
    while run:
        updated_rects = []
        current_mouse_pos = pygame.mouse.get_pos()

        # process events
        for event in pygame.event.get():
            if event.type == pgl.QUIT:
                run = False
                break

            elif event.type == pgl.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                row, col = find_click_rect(current_mouse_pos)
                if left:# process left clicks
                    mouse_pos = event.pos
                    for sprite in active_group.sprites()[::-1]:
                        if sprite.rect.collidepoint(mouse_pos):
                            start_pos = grid[row][col]
                            moving_group.add(sprite)
                            active_group.remove(sprite)
                            break

            elif event.type == pgl.MOUSEMOTION and len(moving_group):
                mouse_pos = event.pos
                for sprite in moving_group.sprites()[::-1]:
                    end_pos = access_two_d(grid,find_click_rect(mouse_pos))
                    if start_pos != end_pos:
                        sprite.rect = Rect(end_pos[0]+10, end_pos[1]+10, 128, 180)
                        active_group.add(sprite)
                        break

            elif event.type == pgl.MOUSEBUTTONUP:
                if len(moving_group):
                    for sprite in moving_group:
                        moving_group.remove(sprite)
                        active_group.add(sprite)


        #remove or add sprites in active, then draw screen
        updated_rects.extend(background_group.draw(screen))
        updated_rects.extend(active_group.draw(screen))
        updated_rects.extend(moving_group.draw(screen))
        pygame.display.update(updated_rects)
    pygame.quit()

if __name__ == "__main__":
    main()
    print("Finished")