#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame

class Player:

    def __init__(self, logger = None):
        try:
            self.up = pygame.image.load("img/pacman_up3.png").convert_alpha()
            self.down = pygame.image.load("img/pacman_down3.png").convert_alpha()
            self.left = pygame.image.load("img/pacman_left3.png").convert_alpha()
            self.right = pygame.image.load("img/pacman_right3.png").convert_alpha()
        except pygame.error, message:
            raise SystemExit, message
        self.logger = logger
        self.direction = self.right

    #Move the Player position
    def move(self, direction, map, displayer):
        width = displayer.wall.get_size()[0]
        height = displayer.wall.get_size()[1]
        right = self.x + self.direction.get_size()[0]
        bottom = self.y + self.direction.get_size()[1]

        if direction == "right":
            if all(map.map[self.y / height][(right + 2) / width] != c for c in ('1', '2', '3'))\
            and all(map.map[bottom / height][(right + 2) / width] != c for c in ('1', '2', '3')):
                self.x += 1
                self.direction = self.right
        elif direction == "left":
            if all(map.map[self.y / height][(self.x - 2) / width] != c for c in ('1', '2', '3'))\
            and all(map.map[bottom / height][(self.x - 2) / width] != c for c in ('1', '2', '3')):
                self.x -= 1
                self.direction = self.left
        elif direction == "up":
            if all(map.map[(self.y - 2) / height][self.x / width] != c for c in ('1', '2', '3'))\
            and all(map.map[(self.y - 2) / width][right / width] != c for c in ('1', '2', '3')):
                self.y -= 1
                self.direction = self.up
        elif direction == "down":
            if all(map.map[(bottom + 2) / height][self.x / width] != c for c in ('1', '2', '3'))\
            and all(map.map[(bottom + 2) / height][right / width] != c for c in ('1', '2', '3')):
                self.y += 1
                self.direction = self.down
        map.end[0] = (self.x + (self.direction.get_size()[0] / 2)) / displayer.x
        map.end[1] = (self.y + (self.direction.get_size()[0] / 2)) / displayer.y
        
        self.pac_rect = pygame.Rect(self.x, self.y, self.direction.get_size()[0], self.direction.get_size()[1])

    #Set the position of the Player
    def set_position(self, map, displayer):
        i = 0
        while i < len(map.map):
            j = 0;
            while j < len(map.map[i]):
                if map.map[i][j] == 'A':
                    self.x = j * displayer.x + (self.direction.get_size()[0] / 2)
                    self.y = i * displayer.y + (self.direction.get_size()[1] / 2)
                    i = 999
                    break
                j += 1
            i += 1
            
        self.pac_rect = pygame.Rect(self.x, self.y, self.direction.get_size()[0], self.direction.get_size()[1])

