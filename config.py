import pygame as pg

BOARD_SIZE = COLUMNS, ROWS = 8, 8
SCREEN_WIDTH, SCREEN_HEIGHT = None, None
COLOR_THEME = [[(235, 236, 208), (115, 149, 82)], [None]]
MARGIN_PERCENTAGE = 0.8 # any resized width must be greater than (height + height * MARGIN_PERCENTAGE)
MIN_SIZE_Y = 400
MIN_SIZE_X = 400 + (MARGIN_PERCENTAGE * MIN_SIZE_Y)

PIECE_SCALE = 252.083
CIRCLE_SCALE = 0.6 # Determines diameter relative to the size of the square