from turtle import screensize
from constants import *
import numpy as np
import pygame
import random
import sys



class ScoreManager:
    def __init__(self):
        self.score = 0
        
        
    def reset_score(self):
        self.score

class Menu:

    def __init__(self, screen):
        #SCREEN
        self.screen = screen
        
        #TRANPARENT SCREEN
        self.transparent_screen = pygame.Surface( (BOARD_WIDTH, BOARD_HEIGHT) )
        self.transparent_screen.set_alpha( TRANSPARENT_ALPHA )
        self.transparent_screen.fill( WHITE )
        self.transparent_screen_pos = (XSHIFT, YSHIFT3)

        # GAME OVER
        self.go_font = pygame.font.SysFont('verdana', 30, True)
        self.go_lbl = self.go_font.render('Game over!', 1, GAMEOVER_LBL_COLOR)
        self.go_pos = (XSHIFT + BOARD_WIDTH//2 - self.go_lbl.get_rect().width//2, YSHIFT3 + BOARD_HEIGHT//2 - self.go_lbl.get_rect().height//2 - 35)

        #TRY AGAIN
        self.tryagain_btn = pygame.image.load('tryagain.png')
        self.tryagain_btn = pygame.transform.scale(self.tryagain_btn, (115, 48))
        self.tryagain_btn_pos = (XSHIFT + BOARD_WIDTH//2 - self.tryagain_btn.get_width()//2, YSHIFT3 + BOARD_HEIGHT//2 - self.tryagain_btn.get_height()//2 + 35)
        self.tryagain_btn_rect = self.tryagain_btn.get_rect(topleft=self.tryagain_btn_pos)

        #VARS
        self.active = False
    
    def show(self):
        if self.active:
            #TRANSPARENT SCREEN
            self.screen.blit(self.transparent_screen, self.transparent_screen_pos)

            #GAME OVER LBL
            self.screen.blit(self.go_lbl, self.go_pos)

            #TRY AGAIN BTN
            self.screen.blit(self.tryagain_btn, self.tryagain_btn_pos)

    def hide(self, bg):
        self.active = False

        pygame.draw.rect(self.screen, BOARD_COLOR, bg)


class GUI:

    def __init__(self, screen):
        #SCREEEN
        self.screen = screen

        #LOGO
        self.logo = pygame.image.load('logo.png')
        self.logo = pygame.transform.scale(self.logo, (170, 50))#(self.logo.get_width()//2, self.logo.get_height()//2))
        self.logo_pos = (80, YSHIFT)

        #SCORE RECT
        self.score_rect = pygame.image.load('score.png')
        self.score_rect = pygame.transform.scale(self.score_rect, (110, 42))
        self.score_rect_pos = (240, YSHIFT)

        
        #SCPRE VALUE
        self.score_font = pygame.font.SysFont('verdana', 20, bold=True)

        # #MESSAGE
        self.message = pygame.image.load('message.png')
        self.message = pygame.transform.scale(self.message, (210, 50))#(self.message.get_width()//2, self.message.get_height()//2)) 
        self.message_pos = (XSHIFT, YSHIFT2)

        #NEW GAME  
        self.newgame_btn = pygame.image.load('newgame.png')
        self.newgame_btn = pygame.transform.scale(self.newgame_btn, (125, 50))
        self.newgame_btn_pos = (XSHIFT3, YSHIFT2)
        self.newgame_btn_rect = self.newgame_btn.get_rect(topleft=self.newgame_btn_pos)

        #BOARD
        self.board_rect = (XSHIFT, YSHIFT3, BOARD_WIDTH, BOARD_HEIGHT)

        #MENU
        self.menu = Menu( screen )


    def show_start(self):
        #LOGO
        self.screen.blit(self.logo, self.logo_pos)

        #SCORE
        self.screen.blit(self.score_rect, self.score_rect_pos)

        #MESSAGE
        self.screen.blit(self.message, self.message_pos)

        #NEW GAME
        self.screen.blit(self.newgame_btn, self.newgame_btn_pos)

        #BOARD
        pygame.draw.rect(self.screen, BOARD_COLOR, self.board_rect)


    def update_scores(self, score_value):
        #SCORE RECT
        self.screen.blit(self.score_rect, self.score_rect_pos)

        #SCORE VALUE
        self.score_lbl = self.score_font.render(str(score_value), 0, WHITE)
        self.score_lbl_pos = (240 + self.score_rect.get_width()//2 - self.score_lbl.get_rect().width//2, 20 + self.score_rect.get_height()//2 - self.score_lbl.get_rect().height//2 + 8)
        self.screen.blit(self.score_lbl, self.score_lbl_pos)

        
    def action_listener(self, event):
        #MENU
        if self.menu.active:
            if self.menu.tryagain_btn_rect.collidepoint(event.pos):
                self.menu.hide(self.board_rect)
                return True
        
        #TRY AGAIN BTN
        elif self.newgame_btn_rect.collidepoint(event.pos):
            return True
        
        return False

        
class Game:

    def __init__(self, screen):
        #SCREEEN
        self.screen = screen
        #TILES
        self.tiles = np.zeros((ROWS, COLS))
        #GUI
        self.gui = GUI(screen)
        #SCORES
        self.score_manager = ScoreManager()
        #LABLE FONT
        self.lbl_font = pygame.font.SysFont('verdana', 30, bold=True)
        #VAR
        self.generate = False
        self.playing = True

    def draw_board(self):
        rShift, cShift = GAP, GAP
        for row in range(ROWS):
            for col in range(COLS):
                tile_num = int(self.tiles[row][col])

                #TILE
                tile_color = TILES_COLORS[tile_num]
                pygame.draw.rect(self.screen, tile_color, (XSHIFT + cShift + col * TILE_SIZE, YSHIFT3 + rShift + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                #LABEL
                tile_lbl_color = LBLS_COLORS[tile_num]
                lbl = self.lbl_font.render(str(tile_num), 0, tile_lbl_color)
                lbl_pos = (XSHIFT + cShift + col * TILE_SIZE + TILE_SIZE//2 - lbl.get_rect().width//2, YSHIFT3 + rShift + row * TILE_SIZE + TILE_SIZE//2 - lbl.get_rect().height//2)
                self.screen.blit(lbl, lbl_pos)

                cShift += GAP
            
            rShift += GAP
            cShift = GAP

    def generate_tiles(self):
        empty_tiles = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0: empty_tiles.append((row, col))

        idx = random.randrange(0, len(empty_tiles))
        row, col = empty_tiles[idx]
        rnd = random.randint(1,10)
        tile_value = 2
        if rnd > 7: tile_value = 4
        self.tiles[row][col] = tile_value

    def __move_and_merge(self, direction, row, col):
        dx, dy = 0, 0
        if direction == 'UP': dy = -1
        elif direction == 'DOWN': dy = 1
        elif direction == 'RIGHT': dx = 1
        elif direction == 'LEFT': dx = -1

        try:
            #MOVE
            if self.tiles[row +dy][col + dx] == 0:
                value = self.tiles[row][col]
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] = value
                self.generate = True
                self.__move_and_merge(direction, row + dy, col + dx)
            elif self.tiles[row][col] == self.tiles[row + dy][col + dx]:
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] *= 2
                self.score_manager.score += int(self.tiles[row + dy][col + dx])
                self.generate = True
        except IndexError: return
    
    def slide_tiles(self, direction):
        #UP
        if direction == 'UP':
            for row in range(1, ROWS):
                for col in range(COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)
        
        #DOWN
        if direction == 'DOWN':
            for row in range(ROWS-2, -1, -1):
                for col in range(COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

        #RIGHT
        if direction == 'RIGHT':
            for row in range(ROWS):
                for col in range(COLS-2, -1, -1):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

        #LEFT
        if direction == 'LEFT':
            for row in range(ROWS):
                for col in range(1, COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)
    
    def __full_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0: return False
        return True

    def __no_more_moves(self):
        #UP
        for row in range(1, ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row-1][col]: return False
        
        #DOWN
        for row in range(ROWS-2, -1, -1):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row+1][col]: return False

        #RIGHT
        for row in range(ROWS):
            for col in range(COLS-2, -1, -1):
                if self.tiles[row][col] == self.tiles[row][col+1]: return False

        #LEFT
        for row in range(ROWS):
            for col in range(1, COLS):
                if self.tiles[row][col] == self.tiles[row][col-1]: return False

        return True

    def is_game_over(self):
        if self.__full_board():
            return self.__no_more_moves()

    def new(self):
        self.tiles = np.zeros( (ROWS, COLS) )
        self.score_manager.reset_score()
        self.generate_tiles()

            
def main():

    #PYGAME
    pygame.init()
    screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
    pygame.display.set_caption('2048')
    screen.fill(SCREEN_COLOR)

    #OBJECTS
    game = Game(screen)

    #INIT

    #GUI initial call
    game.gui.show_start()

    #Initial tiles displayed
    n = random.randint(1, 2)
    for i in range(n): game.generate_tiles()


    #MAINLOOP
    while game.playing:

        #UPDATE BOARD GAME
        game.draw_board()

        #Menu?
        game.gui.menu.show()

        #Update Scores
        game.gui.update_scores(game.score_manager.score)

        #Events
        for event in pygame.event.get():

            #QUIT
            if event.type == pygame.QUIT:
                sys.exit()

            #KEYDOWN
            if event.type == pygame.KEYDOWN:

                #UP
                if event.key == pygame.K_UP:
                    game.slide_tiles('UP')
                
                #DOWN
                if event.key == pygame.K_DOWN:
                    game.slide_tiles('DOWN')

                #RIGHT
                if event.key == pygame.K_RIGHT:
                    game.slide_tiles('RIGHT')

                #LEFT
                if event.key == pygame.K_LEFT:
                    game.slide_tiles('LEFT')

                #NEW TILES ?
                if game.generate:
                    game.generate_tiles()
                    game.generate = False

            #MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game.gui.action_listener(event):
                        game.new()

        if game.is_game_over():
            game.gui.menu.active = True

        pygame.display.update()

main()
