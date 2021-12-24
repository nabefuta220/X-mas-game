"""
処理の作成
"""
from typing import Tuple
import pygame
import sys

from pygame.constants import KEYDOWN, K_q
from model import box_size


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
        クリックしたボックスの座標(左上を原点とする)
        そのような座標がなければNoneとする
    """
    global box_size
