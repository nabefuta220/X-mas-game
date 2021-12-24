import pygame
from controll import check_events

from model import _VARS, GREEN, SCREENSIZE,row,column
from view import draw_grid

def main():
    """
    実行用の関数
    """
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        check_events()
        _VARS['surf'].fill(GREEN)
        draw_grid(row, column)
        pygame.display.update()


if __name__ == "__main__":
    main()
