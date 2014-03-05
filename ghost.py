#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame
import AStar

class Ghost:

    def __init__(self, map, logger = None):
        try:
            self.up = pygame.image.load("img/ghost_up2.png").convert_alpha()
            self.down = pygame.image.load("img/ghost_down2.png").convert_alpha()
            self.left = pygame.image.load("img/ghost_left2.png").convert_alpha()
            self.right = pygame.image.load("img/ghost_right2.png").convert_alpha()
        except pygame.error, message:
            raise SystemExit, message
        self.logger = logger
        self.loop = 0
        self.direction = self.left
        self.map_one_d = []
        self.sizex_by2 = self.direction.get_size()[0] / 2
        self.sizey_by2 = self.direction.get_size()[1] / 2
        i = 0

        #Create a 1 dimension list of the map for AStar
        while i < len(map.map):
            self.map_one_d.extend(map.map[i])
            i += 1
        j = 0
        while j < len(self.map_one_d):
            if self.map_one_d[j] == 'D' or self.map_one_d[j] == 'A':
                self.map_one_d[j] = '0'
            if self.map_one_d[j] == '2' or self.map_one_d[j] == '3':
                self.map_one_d[j] = '1'
            j += 1

        #Create Astar Instance
        self.astar = AStar.AStar(AStar.SQ_MapHandler(self.map_one_d, len(map.map[0]), len(map.map)))

    #Set positions of the ghost
    def set_position(self, map, displayer):
        i = 0
        while i < len(map.map):
            j = 0;
            while j < len(map.map[i]):
                if map.map[i][j] == 'D':
                    self.x = j * displayer.x + self.sizex_by2
                    self.y = i * displayer.y + self.sizey_by2
                    self.old_path = (j, i)
                    self.savepath = (j, i)
                    i = 9999
                    break
                j += 1
            i += 1

    def check_wall(self, direction,  map, displayer):
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


    #Move the ghost thanks to path given by AStar
    def move(self, map, displayer, pacman):
        self.find_path(map)

        if self.path: 
            if self.path[0] != self.savepath or self.check_path() != 0:
                self.old_path = (((self.x + self.sizex_by2) / displayer.x), ((self.y + self.sizey_by2) / displayer.y))
                self.savepath = self.path[0]


            if self.old_path[0] > self.path[0][0]:
               self.check_wall("left", map, displayer)
            elif self.old_path[0] < self.path[0][0]:
               self.check_wall("right", map, displayer)
            elif self.old_path[1] > self.path[0][1]:
               self.check_wall("up", map, displayer)
            elif self.old_path[1] < self.path[0][1]:
               self.check_wall("down", map, displayer)
            else:
                self.find_path(map)

            if float(self.x) == float(self.path[0][0] * displayer.x + self.sizex_by2): 
                map.start[0] = (self.x + self.sizex_by2) / displayer.x

            if float(self.y) == float(self.path[0][1] * displayer.y + self.sizey_by2): 
                map.start[1] = (self.y + self.sizey_by2) / displayer.y

            self.ghost_rect = pygame.Rect(self.x, self.y, self.sizex_by2 * 2, self.sizey_by2 * 2)
            #print self.path[0], self.savepath, self.old_path
    
    #Check if the ghost is deviating from his path
    def check_path(self):
        if self.savepath[0] > self.old_path[0]:
            diffx = self.savepath[0] - self.old_path[0]
        else:
            diffx = self.old_path[0] - self.savepath[0]

        if self.savepath[1] > self.old_path[1]:
            diffy = self.savepath[1] - self.old_path[1]
        else:
            diffy = self.old_path[1] - self.savepath[1]

        if diffx >= 2 or diffy >= 2 or (diffx >= 1 and diffy >= 1):
            return (1)
        else:
            return (0)

    #launch a AStar algorithm to find the path between the ghost and the player
    def find_path(self, map):
        self.path = []
        start = AStar.SQ_Location(map.start[0], map.start[1])
        end = AStar.SQ_Location(map.end[0], map.end[1])
        p = self.astar.findPath(start, end)
        if p:
            for n in p.nodes:
                self.path.append((n.location.x, n.location.y))


