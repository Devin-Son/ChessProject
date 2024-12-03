import pygame as pg
from config import *
from game import *
from reader import *
from sys import exit
import os

class Game:
    def __init__(self):
        pg.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = MIN_SIZE_X, MIN_SIZE_Y
        self.DISPLAYSURF = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pg.RESIZABLE)
        self.DISPLAYSURF.fill((48, 46, 43))
        pg.display.set_caption('Chess Openings')
        icon = pg.image.load('resources/icon.ico')
        pg.display.set_icon(icon)
        self.board = Board(BOARD_SIZE, self)
        self.board.show_board(self)
        self.board.show_pieces(self)

    def update(self):
        self.board.show_board(self)
        self.board.show_pieces(self)
        self.board.show_legal()
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    self.board.get_click(mouse_pos, game)
            elif event.type == pg.VIDEORESIZE:
                self.SCREEN_HEIGHT = max(event.h, MIN_SIZE_Y)
                self.SCREEN_WIDTH = max(event.w, self.SCREEN_HEIGHT + int(MARGIN_PERCENTAGE * self.SCREEN_HEIGHT))

                if (event.w or event.h):
                    self.DISPLAYSURF = pg.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pg.RESIZABLE)
                    self.DISPLAYSURF.fill((48, 46, 43))
                    self.board.resize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)


    def run(self):
        while True:
            self.check_events()
            self.update()

if __name__ == '__main__':
    game = Game()
    game.board.place_piece(Rook('white', 'h6', game.board))
    game.board.place_piece(Pawn('white', 'd6', game.board))
    game.update()
    game.run()