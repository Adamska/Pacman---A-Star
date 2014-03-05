#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame

class Displayer:

    def __init__(self, logger = None):
	try:
	    self.wall = pygame.image.load("img/Game/wall4.png").convert()
	    self.wall2 = pygame.image.load("img/Game/wall2.png").convert()
	    self.wall3 = pygame.image.load("img/Game/wall3.png").convert()
            self.token = pygame.image.load("img/food3.png").convert_alpha()
            self.tab = []
            self.tab.append(pygame.image.load("img/zero2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/one2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/two2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/three2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/four2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/five2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/six2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/seven2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/eight2.png").convert_alpha())
            self.tab.append(pygame.image.load("img/nine2.png").convert_alpha())
        except pygame.error, message:  
	    print ("Unable to load wall.jpg")
            raise SystemExit, message
        self.x = self.wall.get_size()[0]
        self.y = self.wall.get_size()[1] 
        self.food_x = self.token.get_size()[0]
        self.food_y = self.token.get_size()[1]
        self.logger = logger

    #Display the walls of the map
    def display(self, screen, map):
	i = 0
	while i < len(map.map):
	    j = 0
	    while (j < len(map.map[i])):
		if map.map[i][j] == '1':
		   screen.blit(self.wall, (j * self.x, i * self.y))
                elif map.map[i][j] == '2':
		   screen.blit(self.wall2, (j * self.x, i * self.y))
                elif map.map[i][j] == '3':
		   screen.blit(self.wall3, (j * self.x, i * self.y))
                j += 1
	    i += 1

    #Display the score
    def display_score(self, screen, map, size):
        list = []
        score_tmp = map.score

        if score_tmp == 0:
            list.append(0)
        while (score_tmp != 0):
            list.append(score_tmp % 10)
            score_tmp /= 10

        i = 1
        myfont = pygame.font.SysFont("kinari", 15)
        label = myfont.render("Score : ", 1, (255, 255, 255))
        screen.blit(label, (size[0] - (self.tab[0].get_size()[0] * len(list)) - (len(list) * 3) - label.get_size()[0] - 5, size[1] + 1))
        for nb in list:
            screen.blit(self.tab[nb], (size[0] - (self.tab[nb].get_size()[0] * i) - (i * 3), size[1] + 1, self.tab[nb].get_size()[0], self.tab[nb].get_size()[1]))
            i += 1
    #Display the tokens on the map
    def display_token(self, screen, map):
	i = 0
	while i < len(map.map):
	    j = 0
	    while (j < len(map.map[i])):
                if map.map[i][j] == '0':
                   screen.blit(self.token, (j * self.x + (self.x / 2) - (self.food_x / 2), i * self.y + (self.y / 2) - (self.food_y / 2)))
		j += 1
	    i += 1

    #Display the path of AStar
    def display_path(self, screen, path):
        square = pygame.Surface((self.x, self.y))
        square.fill((100, 0, 0))
        i = 1
        for n in path:
            screen.blit(square, (n[0] * self.x, n[1] * self.y))
            myfont = pygame.font.SysFont("kinari", 20)
            label = myfont.render(str(i), 1, (50,50,150))
            screen.blit(label, (n[0] * self.x + (self.x / 2), n[1] * self.y + (self.y / 2)))
            i += 1

