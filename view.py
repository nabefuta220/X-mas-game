"""
表示に関わる部分の作成
"""
import sys
from typing import Tuple

import pygame
from pygame import sprite
from pygame.locals import KEYDOWN, K_q
from pygame.version import ver
from pygame.sprite import Sprite
from controll import calc_box_size, calc_center_position
from model import _VARS, BLACK, HEIGHT, PADLEFTRIGHT, PADTOPBOTTOM, SCREENSIZE, WIDTH, row, column


class precent_box(Sprite):
    """
    ボックスを表示するクラス
    """

    def __init__(self, position: Tuple[int, int], size: int):
        """
        画像の初期化

        Parameters
        ----------
        position : (int,int)
            中心の座標
        size : int
            画像のサイズ
        """
        super(precent_box, self).__init__()
        self.image = (pygame.image.load('img/precent.png'))
        self.rect = position
        self.image = pygame.transform.scale(
            self.image, (int(size), int(size)))

    def update(self):
        """
        1フレームごとに更新を行う
        """
        pass

    def rotate_center_image(self):
        """
        画像の中心で回転する
        """
        # 画像の傾きを設定
        self.image_angle -= 10
        if self.image_angle <= -360:
            self.image_angle = 0

        # 画像を回転
        rot_image = pygame.transform.rotate(self.image, self.image_angle)
        rot_rect = rot_image.get_rect()
        rot_rect.center = self.image_center_position  # 中心位置を設定(移動)

        # 結果を格納
        self.image = rot_image
        self.rect = rot_rect


def draw_grid(row: int, column: int):
    """
    縦がrow,横がcolnmnの盤面を作成する

    Parameters
    -----------
    row : int
        縦
    column : int
        横
    """
    # サイズを取得する
    box_size = calc_box_size(row, column)

    # 上限・下限の設定
    left = PADLEFTRIGHT
    right = PADLEFTRIGHT+box_size*column
    up = PADTOPBOTTOM
    bottom = PADTOPBOTTOM + box_size*row
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
            (0 + PADLEFTRIGHT+box_size*x, up),
            (0 + PADLEFTRIGHT+box_size*x, bottom), 2)
    for y in range(row):
        # 縦に分ける
        pygame.draw.line(
            _VARS['surf'], BLACK,
            (left, 0 + PADTOPBOTTOM + box_size*y),
            (right, 0 + PADTOPBOTTOM + box_size*y), 2)
     # スプライトのオブジェクトを作ってグループ化


def draw_box(row: int, column: int, flags):
    """
    また開けていないボックスを描画する

    Parameters
    ----------
    row : int
        縦
    column : int
        横
    flag : any
        開けているかのフラグ
    """
    box_size = calc_box_size(row, column)

    boxes = []
    for row_i in range(row):
        for column_i in range(column):
            boxes.append(precent_box(
                calc_center_position((row_i, column_i)), box_size))
    my_group = pygame.sprite.Group(boxes)
    my_group.update()
    my_group.draw(_VARS['surf'])
