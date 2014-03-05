#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import GameRessources
import sys
import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, QUIT, K_RETURN, K_LEFT, K_RIGHT
import displayer
import os 

def usage(msg = ""):
    print("\033[20;32m")
    print(msg)
    print("\033[20;33mUsage :")
    print("./303make <map>")
    print("\033[40;00m")
    raise SystemExit

if __name__ == '__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    #Pygame initialisation
    pygame.init()
    screen = pygame.display.set_mode((1024, 800), DOUBLEBUF, 32)
    pygame.display.set_caption("304Pacman")

    #Create a container for game resources
    game = GameRessources.Game()

    #Create the displayer
    displayer = displayer.Displayer(game.logger);

    try:
        wallpaper = pygame.image.load("img/Menu/wallpaper.png").convert()
        title = pygame.image.load("img/Menu/Title.png").convert_alpha()
        play = pygame.image.load("img/Menu/Play.png").convert_alpha()
        play_s = pygame.image.load("img/Menu/Play_selected.png").convert_alpha()
        options = pygame.image.load("img/Menu/Options.png").convert_alpha()
        options_s = pygame.image.load("img/Menu/Options_selected.png").convert_alpha()

        option_title = pygame.image.load("img/Menu/Menu_options.png").convert_alpha()
        map_opt = pygame.image.load("img/Menu/map_opt.png").convert_alpha()
        map_opt_s = pygame.image.load("img/Menu/map_opt_selected.png").convert_alpha()
        level1 = pygame.image.load("img/Menu/level1.png").convert_alpha()
        level1_s = pygame.image.load("img/Menu/level1_selected.png").convert_alpha()
        level2 = pygame.image.load("img/Menu/level2.png").convert_alpha()
        level2_s = pygame.image.load("img/Menu/level2_selected.png").convert_alpha()  
        tracking = pygame.image.load("img/Menu/tracking.png").convert_alpha()
        tracking_s = pygame.image.load("img/Menu/tracking_selected.png").convert_alpha()
        yes = pygame.image.load("img/Menu/yes.png").convert_alpha()
        yes_s = pygame.image.load("img/Menu/yes_selected.png").convert_alpha()
        no = pygame.image.load("img/Menu/No.png").convert_alpha()
        no_s = pygame.image.load("img/Menu/No_selected.png").convert_alpha()
        go_back = pygame.image.load("img/Menu/go_back.png").convert_alpha()
        go_back_s = pygame.image.load("img/Menu/go_back_selected.png").convert_alpha()
        
    except pygame.error(), message:
        raise SystemExit, message
    
    try:
        with open('score', 'r+') as file_score:
            line = file_score.readline().rstrip('\n')
            if (line != ""):
                game.score_one = line
            line = file_score.readline().rstrip('\n')
            if (line != ""):
                game.score_two = line
    except IOError, message:
        print message

    #Launch menu loop
    menu = 0
    select = 0
    track = 0
    level = 1
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_RETURN:
                    if menu == 0:
                        if select == 0:

                            #Set the music of the game
                            game.setMusic()

                            #Launch the gameLoop
                            game.reset(screen, displayer, track, level)
                            game.gameLoop(screen, displayer)
                            pygame.key.set_repeat()
                        else:
                            menu = 1
                            select = 0
                    if menu == 1 and select == 2:
                        menu = 0
                        select = 0
                elif event.key == K_UP:
                    if select > 0:
                        select -= 1
                elif event.key == K_DOWN:
                    if menu == 0 and select < 1:
                        select += 1
                    elif menu == 1 and select < 2:
                        select += 1
                elif menu == 1 and event.key == K_LEFT:
                    if select == 1 and track > 0:
                        track -= 1
                    elif select == 0 and level > 1:
                        level -= 1

                elif menu == 1 and event.key == K_RIGHT:
                    if select == 1 and track < 1:
                        track += 1
                    elif select == 0 and level < 2:
                        level += 1

        screen.blit(wallpaper, wallpaper.get_rect())
        if menu == 0:            
            screen.blit(title, (((1024 - title.get_size()[0]) / 2), 100, title.get_size()[0], title.get_size()[1]))
            if select == 0:
                screen.blit(play_s, (((1024 - play_s.get_size()[0]) / 2) , 100 + title.get_size()[1] + 190, play_s.get_size()[0], play_s.get_size()[1]))
                screen.blit(options, (((1024 - options.get_size()[0]) / 2) , 100 + title.get_size()[1] + 200 + play_s.get_size()[1] + 100, options.get_size()[0], options.get_size()[1]))
            else:
                screen.blit(play, (((1024 - play.get_size()[0]) / 2) , 100 + title.get_size()[1] + 200, play.get_size()[0], play.get_size()[1]))
                screen.blit(options_s, (((1024 - options_s.get_size()[0]) / 2) , 100 + title.get_size()[1] + 210 + play.get_size()[1] + 100, options_s.get_size()[0], options_s.get_size()[1]))
        else:
            screen.blit(option_title, (((1024 - option_title.get_size()[0]) / 2), 50, option_title.get_size()[0], option_title.get_size()[1]))
            my_font = pygame.font.SysFont("kinari", 30)
            label = my_font.render("Best Score : " + str(game.score_one), 1, (255,255,255))
            label2 = my_font.render("Best Score : " + str(game.score_two), 1, (255,255,255))
            screen.blit(label, (40 + map_opt_s.get_size()[0] + 75 + (level1.get_size()[0] / 2) - (label.get_size()[0] / 2), 40 + option_title.get_size()[1] + 100 - 20))
            screen.blit(label2, (40 + map_opt_s.get_size()[0] + 75 + level1.get_size()[0] + 50 + (level2.get_size()[0] / 2) + 25 - (label2.get_size()[0] / 2), 40 + option_title.get_size()[1] + 100 - 20))
            if select == 0:
                screen.blit(map_opt_s, (40, 40 + option_title.get_size()[1] + 100, map_opt_s.get_size()[0], map_opt_s.get_size()[1]))
                if level == 1:    
                    screen.blit(level1_s, (40 + map_opt_s.get_size()[0] + 75, 40 + option_title.get_size()[1] + 100, level1_s.get_size()[0], level1_s.get_size()[1]))
                    screen.blit(level2, (50 + map_opt_s.get_size()[0] + 75 + level1_s.get_size()[0] + 50, 50 + option_title.get_size()[1] + 100, level2.get_size()[0], level2.get_size()[1]))
                else:
                    screen.blit(level1, (50 + map_opt_s.get_size()[0] + 75, 50 + option_title.get_size()[1] + 100, level1.get_size()[0], level1.get_size()[1]))
                    screen.blit(level2_s, (60 + map_opt_s.get_size()[0] + 75 + level1.get_size()[0] + 50, 40 + option_title.get_size()[1] + 100, level2_s.get_size()[0], level2_s.get_size()[1]))
                screen.blit(tracking, (50, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, tracking.get_size()[0], tracking.get_size()[1]))
                if track == 0:
                    screen.blit(yes_s, (40 + tracking.get_size()[0] + 100, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, yes_s.get_size()[0], yes_s.get_size()[1]))
                    screen.blit(no, (50 + tracking.get_size()[0] + 100 + yes.get_size()[0] + 50, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, no.get_size()[0], no.get_size()[1]))
                else:
                    screen.blit(yes, (50 + tracking.get_size()[0] + 100, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, yes.get_size()[0], yes.get_size()[1]))
                    screen.blit(no_s, (47 + tracking.get_size()[0] + 100 + yes.get_size()[0] + 50, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, no_s.get_size()[0], no_s.get_size()[1]))
                screen.blit(go_back, (50, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150 + tracking.get_size()[1] + 150, go_back.get_size()[0], go_back.get_size()[1]))
            elif select == 1:
                screen.blit(map_opt, (50, 50 + option_title.get_size()[1] + 100, map_opt.get_size()[0], map_opt.get_size()[1]))
                if level == 1:    
                    screen.blit(level1_s, (40 + map_opt_s.get_size()[0] + 75, 40 + option_title.get_size()[1] + 100, level1_s.get_size()[0], level1_s.get_size()[1]))
                    screen.blit(level2, (50 + map_opt_s.get_size()[0] + 75 + level1_s.get_size()[0] + 50, 50 + option_title.get_size()[1] + 100, level2.get_size()[0], level2.get_size()[1]))
                else:
                    screen.blit(level1, (50 + map_opt_s.get_size()[0] + 75, 50 + option_title.get_size()[1] + 100, level1.get_size()[0], level1.get_size()[1]))
                    screen.blit(level2_s, (60 + map_opt_s.get_size()[0] + 75 + level1.get_size()[0] + 50, 40 + option_title.get_size()[1] + 100, level2_s.get_size()[0], level2_s.get_size()[1]))
                screen.blit(tracking_s, (40, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, tracking_s.get_size()[0], tracking_s.get_size()[1]))
                if track == 0:
                    screen.blit(yes_s, (40 + tracking.get_size()[0] + 100, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, yes_s.get_size()[0], yes_s.get_size()[1]))
                    screen.blit(no, (33 + tracking.get_size()[0] + 100 + yes_s.get_size()[0] + 50, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, no.get_size()[0], no.get_size()[1]))
                else:
                    screen.blit(yes, (50 + tracking.get_size()[0] + 100, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, yes.get_size()[0], yes.get_size()[1]))
                    screen.blit(no_s, (30 + tracking.get_size()[0] + 100 + yes_s.get_size()[0] + 50, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, no_s.get_size()[0], no_s.get_size()[1]))
                screen.blit(go_back, (50, 49 + option_title.get_size()[1] + 100 + map_opt.get_size()[1] + 150 + tracking_s.get_size()[1] + 150, go_back.get_size()[0], go_back.get_size()[1]))
            else:
                screen.blit(map_opt, (50, 50 + option_title.get_size()[1] + 100, map_opt.get_size()[0], map_opt.get_size()[1]))
                if level == 1:    
                    screen.blit(level1_s, (40 + map_opt_s.get_size()[0] + 75, 40 + option_title.get_size()[1] + 100, level1_s.get_size()[0], level1_s.get_size()[1]))
                    screen.blit(level2, (50 + map_opt_s.get_size()[0] + 75 + level1_s.get_size()[0] + 50, 50 + option_title.get_size()[1] + 100, level2.get_size()[0], level2.get_size()[1]))
                else:
                    screen.blit(level1, (50 + map_opt_s.get_size()[0] + 75, 50 + option_title.get_size()[1] + 100, level1.get_size()[0], level1.get_size()[1]))
                    screen.blit(level2_s, (60 + map_opt_s.get_size()[0] + 75 + level1.get_size()[0] + 50, 40 + option_title.get_size()[1] + 100, level2_s.get_size()[0], level2_s.get_size()[1]))
                screen.blit(tracking, (50, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, tracking.get_size()[0], tracking.get_size()[1]))
                if track == 0:
                    screen.blit(yes_s, (40 + tracking.get_size()[0] + 100, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, yes_s.get_size()[0], yes_s.get_size()[1]))
                    screen.blit(no, (50 + tracking.get_size()[0] + 100 + yes.get_size()[0] + 50, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, no.get_size()[0], no.get_size()[1]))
                else:
                    screen.blit(yes, (50 + tracking.get_size()[0] + 100, 50 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, yes.get_size()[0], yes.get_size()[1]))
                    screen.blit(no_s, (47 + tracking.get_size()[0] + 100 + yes.get_size()[0] + 50, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150, no_s.get_size()[0], no_s.get_size()[1]))
                screen.blit(go_back_s, (40, 40 + option_title.get_size()[1] + 100 + map_opt_s.get_size()[1] + 150 + tracking.get_size()[1] + 150, go_back_s.get_size()[0], go_back_s.get_size()[1]))
        pygame.display.flip()
