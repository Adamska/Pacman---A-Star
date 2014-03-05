#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler
import sys
import map
import player
import ghost
import pygame
from pygame.locals import QUIT, K_ESCAPE, K_p, KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, DOUBLEBUF

class Game:
    def __init__(self):
        self.createLogger()
        self.score_one = "0"
        self.score_two = "0"
        try:
            self.paused = pygame.image.load("img/pause2.png").convert_alpha()
        except pygame.error(), message:
            raise SystemExit, message 

    #Create a logger.
    def createLogger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('pacman.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    #Init the Game
    def reset(self, screen, displayer, track, level):
        #Create the map
        if len(sys.argv) < 2:
            self.map = map.Map(displayer, "maps/level" + str(level), self.logger)
            self.level = level
        else:
            self.map = map.Map(displayer, sys.argv[1], self.logger)
            self.level = 0

        self.track = track
        #Create the pygame window
        self.width = len(self.map.map[0]) * displayer.x
        self.height = len(self.map.map) * displayer.y
        self.size = self.width, self.height + displayer.tab[0].get_size()[1] + 2
        pygame.display.set_mode(self.size, DOUBLEBUF, 32)
        
        #Create the pacman and the ghost
        self.pacman = player.Player(self.logger)
        self.pacman.set_position(self.map, displayer)
        self.ghost = ghost.Ghost(self.map, self.logger)
        self.ghost.set_position(self.map, displayer)
        self.ghost.find_path(self.map)
 
    #Game music
    def setMusic(self):
        try:
            pygame.mixer.music.load("sound/game.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
        except pygame.error, message:
            raise SystemExit, message

    #Manage the pause
    def in_pause(self, pause):
        pause = 1
        while pause == 1:
            for events in pygame.event.get():
                if events.type == QUIT:
                    sys.exit()
                if events.type == KEYDOWN:
                    if events.key == K_ESCAPE:
                        sys.exit()
                    if events.key == K_p:
                        pause = 0
            pygame.time.wait(100)
        return (pause)


    #Game loop
    def gameLoop(self, screen, displayer):
        #Repeater for the keyboard events
        pygame.key.set_repeat(1, 1) 

        pause = 0
        end = 0
        black = 0, 0, 0
        while end == 0:
            #Check events for quit, pause and player's moves
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        end = 1
                    elif event.key == K_p:
                        screen.blit(self.paused, ((self.width - self.paused.get_size()[0]) / 2, (self.height - self.paused.get_size()[1]) / 2, self.paused.get_size()[0], self.paused.get_size()[1]))
                        pygame.display.flip()
                        pause = self.in_pause(pause)
                    elif event.key == K_RIGHT and pause == 0:
                        self.pacman.move("right", self.map, displayer)
                    elif event.key == K_LEFT and pause == 0:
                        self.pacman.move("left", self.map, displayer)
                    elif event.key == K_UP and pause == 0:
                        self.pacman.move("up", self.map, displayer)
                    elif event.key == K_DOWN and pause == 0:
                        self.pacman.move("down", self.map, displayer)
            screen.fill(black)
            self.ghost.move(self.map, displayer, self.pacman)
            if self.pacman.pac_rect.colliderect(self.ghost.ghost_rect) == True:
                end = 1

            #Display the map and its element
            if self.track == 0:
                displayer.display_path(screen, self.ghost.path)
            screen.blit(self.pacman.direction, (self.pacman.x, self.pacman.y))
            self.map.checkToken(self.pacman, self.map)
            displayer.display_token(screen, self.map)
            screen.blit(self.ghost.direction, (self.ghost.x, self.ghost.y))
            displayer.display_score(screen, self.map, (self.width, self.height))
            displayer.display(screen, self.map)
            
            pygame.display.flip()
      
        try:
            with open('score', 'r+') as file_score:
                if (self.level != 0):
                    line = file_score.readline().rstrip('\n')
                    i = 0
                if self.level == 2:
                    i += len(line) + 1
                    line = file_score.readline().rstrip('\n')
                if line == "" or int(line) < self.map.score:
                    file_score.seek(i)
                    file_score.write(str(self.map.score) + "\n")
                if self.level == 1:
                    self.score_one = self.map.score
                else:
                    self.score_two = self.map.score
        except IOError, message:
            print message

        screen = pygame.display.set_mode((1024, 800), DOUBLEBUF, 32)
        pygame.mixer.music.stop()

