"""
処理の作成
"""
from typing import Tuple
import pygame
import sys

from pygame.constants import KEYDOWN, K_q
from model import HEIGHT, PADLEFTRIGHT, PADTOPBOTTOM, WIDTH
from model import row, column


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
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
            get_box_position(pos)


def calc_box_size(row: int, column: int):
    """
    箱のサイズを計算する

    Parameters
    ----------
    row : int
        縦のサイズ
    column : int
        横のサイズ

    Returns
    -------
    box_size : int
        箱のサイズ
    """
    # サイズの限界を取得する
    horizontal_cellsize = (WIDTH - (PADLEFTRIGHT*2))//column
    vertical_cellsize = (HEIGHT - (PADTOPBOTTOM*2))//row

    return min(horizontal_cellsize, vertical_cellsize)


def get_box_position(pos: Tuple[int, int]):
    """
    取得した座標から、どこのボックスをクリックしたか計算する

    Parameters
    ----------
    pos : (int,int)
        クリックした座標

    Returns
    -------
    box_pos : (int,int) | None
        クリックしたボックスの座標(左上を原点とし、(横、縦)する)
        そのような座標がなければNoneとする
    """

    pos_x, pos_y = pos
    box_size = calc_box_size(row, column)
    box_pos_x = (pos_x-PADLEFTRIGHT)//box_size
    box_pos_y = (pos_y-PADTOPBOTTOM) // box_size

    print(box_pos_x, box_pos_y)
    if 0 <= box_pos_x < column and 0 <= box_pos_y < row:
        return(box_pos_x, box_pos_y)
    return None


def calc_center_position(pos: Tuple[int, int]):
    """
    ボックスの中央の座標を取得する

    Paramters
    ---------
    pos : (int,int)
        ボックスの座標(左上を原点とし、(横、縦)する)

    Returns
    -------
    position : (int,int)
        ボックスの中央の座標
    """
    box_size = calc_box_size(row, column)
    pos_x, pos_y = pos
    return(PADLEFTRIGHT + box_size*(pos_y), PADLEFTRIGHT+box_size*(pos_x))
