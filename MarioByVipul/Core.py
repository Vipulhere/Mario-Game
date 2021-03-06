from os import environ

import pygame as pg
from pygame.locals import *

from Const import *
from Map import Map
from MenuManager import MenuManager
from Sound import Sound


class Core(object):
    """

    Main class.

    """
    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(44100, -16, 2, 1024)
        pg.init()
        pg.joystick.init()
        pg.display.set_caption('Mario by MasterVipul')
        pg.display.set_mode((WINDOW_W, WINDOW_H))

        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pg.time.Clock()
        
        # Joystick
        try: # if joystick is connected call init
            self.js = pg.joystick.Joystick(0)
            self.js.init()
        except pg.error:
            print("No Joystick found")
        
        
        
        self.oWorld = Map('1-1')
        self.oSound = Sound()
        self.oMM = MenuManager(self)

        self.run = True
        self.keyR = False
        self.keyL = False
        self.keyU = False
        self.keyD = False
        self.keyShift = False

    def main_loop(self):
        while self.run:
            self.input()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def input(self):
        if self.get_mm().currentGameState == 'Game':
            self.input_player()
        else:
            self.input_menu()

    def input_player(self):
        for e in pg.event.get():

            if e.type == pg.QUIT:
                self.run = False
            
            if e.type == pg.JOYHATMOTION:
                
                hat = self.js.get_hat(0)
                print(hat[1])
                if hat[0] == 1:
                    self.keyR = True
                elif hat[0] == -1:
                    self.keyL = True
                elif hat[0] == 0:
                    self.keyR = False
                    self.keyL = False

               
                if hat[1] == -1:
                    self.keyD = True
                elif hat[1] == 0:
                    self.keyD = False                
            
            if e.type == pg.JOYBUTTONDOWN:
                jump = self.js.get_button(0)
                runNshoot = self.js.get_button(2)
                
                if(jump): self.keyU = True
                if(runNshoot): self.keyShift = True
            
            elif e.type == pg.JOYBUTTONUP:
                jump = self.js.get_button(0)
                runNshoot = self.js.get_button(2)
                
                if jump == 0: self.keyU = False
                if runNshoot == 0: self.keyShift = False
                
            elif e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    self.keyR = True
                elif e.key == K_LEFT:
                    self.keyL = True
                elif e.key == K_DOWN:
                    self.keyD = True
                elif e.key == K_UP:
                    print(self.keyU)
                    self.keyU = True
                elif e.key == K_LSHIFT:
                    self.keyShift = True

            elif e.type == KEYUP:
                if e.key == K_RIGHT:
                    self.keyR = False
                elif e.key == K_LEFT:
                    self.keyL = False
                elif e.key == K_DOWN:
                    self.keyD = False
                elif e.key == K_UP:
                    self.keyU = False
                elif e.key == K_LSHIFT:
                    self.keyShift = False

    def input_menu(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.run = False
            
            elif e.type == pg.JOYBUTTONDOWN:
                start = self.js.get_button(7)
                if(start): self.get_mm().start_loading()
            
            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    self.get_mm().start_loading()

    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def get_map(self):
        return self.oWorld

    def get_mm(self):
        return self.oMM

    def get_sound(self):
        return self.oSound
