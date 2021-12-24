"""
表示に関わる部分の作成
"""
import sys

import pygame
from pygame.locals import KEYDOWN, K_q

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 600, 400
BLACK = (0, 0, 0)
GREEN = (71, 126, 29)
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 60, 60
# VARS:
_VARS = {'surf': False}


def main():
    """
    実行用の関数
    """
    pygame.init()
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    while True:
        check_events()
        _VARS['surf'].fill(GREEN)
        draw_grid(5, 6)
        pygame.display.update()


def draw_grid(row: int, column: int):
    """
    縦がrow,横がcolnmnの盤面を作成する

    Parameters
    -----------
    row : int
        縦
    column : int
        横

    Returns
    -------
    size : int
        画面のサイズ
    """
    # サイズを取得する
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))//column
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))//row

    # サイズをどちらかの最小値に調整する
    horizontal_cellsize = min(horizontal_cellsize, vertical_cellsize)
    vertical_cellsize = horizontal_cellsize

    # 上限・下限の設定
    left = PADLEFTRIGHT
    right = PADLEFTRIGHT+horizontal_cellsize*column
    up = PADTOPBOTTOM
    bottom = PADTOPBOTTOM + vertical_cellsize*row
    # 基準座標の設定
    top_left = (left, up)
    top_right = (right, up)
    bottom_left = (left, bottom)
    bottom_right = (right, bottom)
    pygame.draw.line(_VARS['surf'], BLACK, top_left, top_right, 2)    # 上辺
    pygame.draw.line(_VARS['surf'], BLACK, bottom_left, bottom_right, 2)  # 下辺
    pygame.draw.line(_VARS['surf'], BLACK, top_left, bottom_left, 2)  # 左辺
    pygame.draw.line(_VARS['surf'], BLACK, top_right, bottom_right, 2)  # 右辺

    # 横に分ける
    for x in range(column):
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (0 + PADLEFTRIGHT+horizontal_cellsize*x, up),
            (0 + PADLEFTRIGHT+horizontal_cellsize*x, bottom), 2)
    for y in range(row):
        # 縦に分ける
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (left, 0 + PADTOPBOTTOM + vertical_cellsize*y),
            (right, 0 + PADTOPBOTTOM + vertical_cellsize*y), 2)
    return horizontal_cellsize


def check_events():
    """
    イベントのチェック
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
