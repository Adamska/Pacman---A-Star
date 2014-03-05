#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame

class Map:
    EMPTY = '0'
    WALL = '1'
    GHOST = 'D'
    PLAYER = 'A'

    def __init__(self, displayer, path = '', logger = None):

        #Create and loading map
        self.score = 0
        self.map = []
        if path != '':
            self.load_map(path)
        self.logger = logger

        #Load sounds for the tokens
        try:
            self.sound_eat = pygame.mixer.Sound("sound/pacman_eat.wav")
            self.sound_eat.set_volume(0.2)
        except pygame.error, message:
            raise SystemExit, message

        #Create the list of tokens and remember the positions of pacman and ghost for AStar
        self.tokenList = []
        for i in range(0, len(self.map) - 1):
            for j in range(0, len(self.map[i]) - 1):
                if self.map[i][j] == '0':
                    self.tokenList.append(pygame.Rect(j * displayer.x + (displayer.x / 2) - (displayer.food_x / 2),\
                                          i * displayer.y + (displayer.y / 2) - (displayer.food_y / 2),\
                                          displayer.token.get_size()[0], displayer.token.get_size()[1]))
                elif self.map[i][j] == 'D':
                    self.start = [j, i]
                elif self.map[i][j] == 'A':
                    self.end = [j, i]


    #Load the map from a path
    def load_map(self, path):
        try:
            with open(path, 'r') as f:
                self.map = f.readlines()
            # Convert the map of lines in a 2-dimensions matrix
            self.map = [[y for y in x[:-1]] for x in self.map]
        except IOError as e:
            self.logger.error("Error %s: %s: %s" % (e.errno, e.filename, e.strerror))
        i = 0;
        a = 0
        d = 0
        while i < len(self.map):
            j = 0
            while j < len(self.map[i]):
               if self.map[i][j] == 'A':
                   a += 1
               elif self.map[i][j] == 'D':
                   d += 1
               j += 1
            i += 1
        if a != 1 or d != 1:
            print ("Map must contains only one 'A', one 'D'")
            raise SystemExit

    #Check if pacman pick up a token and remove if it's true 
    def checkToken(self, pacman, map): 
        pac_rect = pygame.Rect(pacman.x, pacman.y, pacman.direction.get_size()[0], pacman.direction.get_size()[1])
        test = pac_rect.collidelist(self.tokenList)
        if test != -1:
            end = 0;
            self.sound_eat.play()
            self.score += 100
            for i in range(0, len(self.map) - 1):
                for j in range(0, len(self.map[i]) - 1):
                    if map.map[i][j] == '0':
                        if end == test:
                            map.map[i][j] = '4'
                        end += 1
            del self.tokenList[test]
