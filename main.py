
import sys
from typing import Dict, Tuple

import pygame
from pygame.constants import KEYDOWN, K_q
from pygame.event import clear
from pygame.sprite import Sprite


SCREENSIZE = WIDTH, HEIGHT = 600, 400
BLACK = (0, 0, 0)
GREEN = (71, 126, 29)
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 60, 60
# VARS:
_VARS = {'surf': False}
row = 5
column = 8


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
        self.size = size
        self.images = [pygame.image.load('img/precent.png'),
                       pygame.image.load('img/precent_with_flag.png')]
        self.rect = position
        self.mode = 0
        self.image = pygame.transform.scale(
            self.images[self.mode], (int(self.size), int(self.size)))

    def update(self):
        """
        1フレームごとに更新を行う
        """
        if self.mode == -1:
            self.kill()
            print("killed")

    def change_flag(self):
        """
        旗を切り替える
        """
        self.mode = not self.mode
        self.image = pygame.transform.scale(
            self.images[self.mode], (int(self.size), int(self.size)))

    def open(self):
        """
        この箱を開く
        """
        self.mode = -1

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


class boxes:
    """
    boxの集合
    """

    def __init__(self, row: int, column: int):
        """
        オブジェクトの初期化
        Parameters
        ----------
        row : int
            縦
        column : int
            横
        """
        box_size = calc_box_size(row, column)
        self.box_list: Dict[Tuple[int, int], precent_box]
        self.box_list = {}
        for row_i in range(row):
            for column_i in range(column):
                self.box_list[(row_i, column_i)] = precent_box(
                    calc_center_position((row_i, column_i)), box_size)
        self.group = pygame.sprite.Group(self.box_list.values())

    def update(self):
        self.group.update()

    def draw(self, surface):
        self.group.draw(surface)

    def change_flag(self, pos):
        """
        posの画像を変更する
        """
        pos_x, pos_y = pos
        self.box_list[(pos_y, pos_x)].change_flag()

    def open(self, pos):
        """
        posの箱を開く
        """
        pos_x, pos_y = pos
        open_pos = (pos_y, pos_x)
        if self.box_list[open_pos].mode == 0:
            self.box_list[open_pos].open()

            #self.box_list[open_pos] = None
            self.group.clear(_VARS['surf'], clear_callback)


def clear_callback(surf, rect):
    color = GREEN
    surf.fill(color, rect)


box = boxes(row, column)


def main():
    """
    実行用の関数
    """
    pygame.init()
    global box
    _VARS['surf'] = pygame.display.set_mode(SCREENSIZE)
    _VARS['surf'].fill(GREEN)
    draw_grid(row, column)
    box.change_flag((0, 1))

    while True:
        check_events()

        box.update()
        box.draw(_VARS['surf'])
        draw_grid(row, column)
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


def check_events():
    """
    イベントのチェック
    """
    global box
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        # クリックされたとき
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos, event.button)
            box_pos = get_box_position(pos)
            if event.button == 3 and box_pos is not None:
                box.change_flag(box_pos)
            if event.button == 1 and box_pos is not None:
                box.open(box_pos)


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


if __name__ == "__main__":
    main()
