import pygame
from controll import check_events

from model import _VARS, GREEN, SCREENSIZE,box_size
from view import draw_grid

def main():
    global box_size
    """
    実行用の関数
    """
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        check_events()
        _VARS['surf'].fill(GREEN)
        box_size = draw_grid(5, 6)
        pygame.display.update()


if __name__=="__main__":
    main()
