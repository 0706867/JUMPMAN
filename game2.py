import pygame
import os
import platform
from pygame import mixer
from pygame.locals import *
import pickle
from os import path

clock = pygame.time.Clock()
fps = 60
screen_w = 960
screen_h = 600

font_score = pygame.font.get_default_font()
font = pygame.font.get_default_font()

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Platformer')



def draw_text(text, font, text_col, x, y):
    #img = font.render(text, True, text_col)
    #screen.blit(img, (x, y))
    pass

class Buttons():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action


platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
level = 1
score = 0

run = True
loaded = False
game_run = False
main = True

def main_menu():
    bg_img = pygame.image.load('bg.png')
    bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h))
    start_img = pygame.image.load('start_btn.png')
    exit_img = pygame.image.load('exit_btn.png')
    restart_img = pygame.image.load('restart_btn.png')
    
    clock.tick(fps)
    screen.blit(bg_img, (0,0))
    global run
    global game_run
    restart_button = Buttons(screen_w //2 - 50, screen_h //2 + 100, restart_img)
    exit_button = Buttons(screen_w //2 - 350, screen_h //2 , exit_img)
    start_button = Buttons(screen_w //2 + 150, screen_h //2, start_img)
    
    if  exit_button.draw():
        run = False
    if start_button.draw():
        main = False
        game_run = True 
    level = 1
    score = 0
    gameover = 0
    score = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

    return run, game_run, restart_button
        

def game():
    tile_size = 24
    gameover = 0
    main = True
    level = 1
    max_levels = 3
    score = 0
    theme = 0

    #colours
    white = (255,255,255)
    blue = (0,0,200)

    #images
    bg_img = pygame.image.load('bg.png')
    bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h))
    block_img = pygame.image.load('block2.png')
    block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
    chain_img = pygame.image.load('chain.png')
    chain_img = pygame.transform.scale(chain_img, (tile_size,tile_size))
    ladder_img = pygame.image.load('ladder.png')
    coin_img = pygame.image.load('coin.png')
    coin_img = pygame.transform.scale(coin_img, (tile_size,tile_size))
    climb_img = pygame.image.load('climb.png')
    climb_img = pygame.transform.scale(climb_img, (tile_size,tile_size))
    restart_img = pygame.image.load('restart_btn.png')
    start_img = pygame.image.load('start_btn.png')
    exit_img = pygame.image.load('exit_btn.png')
    #level 0
    level_1_alt = ['bg.png', 'block2.png', 'ladder.png']

    #level 1    background image            block image             ladder image
    level_1 = ['level 1/ice_bg.png', 'level 1/ice_block.png','level 1/ice_ladder_clear.png']

    #level 2    background image            block image             ladder image
    level_2 = ['level 2/hall_bg.png', 'level 2/hall_block.png','level 2/hall_ladder1.png','level 2/hall_ladder2.png', 'level 2/hall_ladder3.png']

    #level 3    background image            block image             ladder image
    level_3 = ['level 3/desert_bg.png', 'level 3/desert_block.png', 'level 3/desert_ladder.png']

    #level 4    bakcground image            character face             character death face     character idle image
    level_4 = ['level 4/final_bg.png', 'level 4/luke_face.png', 'level 4/luke_death.png', 'level 4/luke_idle.png',
    #enemy idle     enemy idle animation 2  enemy bullet        enemy death face            enemy face              enemy shoot anim
    'enemy/enemy.png','enemy/enemy2.png', 'enemy/bullet.png','enemy/enemy_death.png', 'enemy/enemy_face.png', 'enemy/enemy_shoot.png']

    levels = [level_1, level_2, level_3, level_4]
    bg_img = pygame.image.load(levels[level-1] [0])
    bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h-120))
    block_img = pygame.image.load(levels[level-1] [1])
    block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
    ladder_img = pygame.image.load(levels[level-1] [2]) 
    bg_bottom = pygame.image.load('bg.png')
    bg_bottom = pygame.transform.scale(bg_bottom, (screen_w,screen_h))

    global restart_button
    global game_run
    tile_size = 24
    gameover = 0
    main = True
    level = 1
    max_levels = 3
    score = 0
    theme = 0
    bg_img = pygame.image.load('bg.png')
    bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h))
    block_img = pygame.image.load('block2.png')
    block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
    chain_img = pygame.image.load('chain.png')
    chain_img = pygame.transform.scale(chain_img, (tile_size,tile_size))
    ladder_img = pygame.image.load('ladder.png')
    coin_img = pygame.image.load('coin.png')
    coin_img = pygame.transform.scale(coin_img, (tile_size,tile_size))
    climb_img = pygame.image.load('climb.png')
    climb_img = pygame.transform.scale(climb_img, (tile_size,tile_size))
    restart_img = pygame.image.load('restart_btn.png')
    start_img = pygame.image.load('start_btn.png')
    exit_img = pygame.image.load('exit_btn.png')

    def reset_level(level):
        #player.reset(screen_w //2 , 430)
        #blob_group.empty()
        #lava_group.empty()
        #exit_group.empty()
        #platform_group.empty()
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
        world = World(world_data)

        return world

    class Player():
        def __init__(self, x, y):
            self.reset(x,y)

        def update(self, gameover):
            dx = 0
            dy = 0
            walk_cooldown = 5
            col_thresh = 20
            key = pygame.key.get_pressed()
            if gameover == 0:
                #play when keyboard is connected
                #get key presses
                if (key[pygame.K_SPACE]) and self.jumped == False and self.in_air == False:
                    #jump_fx.play()
                    self.jumped = True
                    self.vel_y = -10
                if (key[pygame.K_SPACE]) == False:
                    self.jumped = False
                if key[pygame.K_LEFT]:
                    dx -= 2
                    self.counter += 1
                    self.direction = -1
                if key[pygame.K_RIGHT] :
                    dx += 2
                    self.counter += 1
                    self.direction = 1
                if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                    self.counter = 0
                    self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]
                
                #only run when playing on the retro pi
                #if os.uname().nodename == 'raspberrypi':
                if os.name == 'raspberrypi':
                    if button_top_left.is_pressed and self.jumped == False and self.in_air == False:
                        #jump_fx.play()
                        self.jumped = True
                        self.vel_y = -10
                    if joystick_up.is_pressed == False:
                        self.jumped = False
                    if joystick_left.is_pressed:
                        dx -= 2
                        self.counter += 1
                        self.direction = -1
                    if joystick_right.is_pressed:
                        dx += 2
                        self.counter += 1
                        self.direction = 1
                    if joystick_left.is_pressed == False and joystick_right.is_pressed == False:
                        self.counter = 0
                        self.index = 0
                        if self.direction == 1:
                            self.image = self.images_right[self.index]
                        if self.direction == -1:
                            self.image = self.images_left[self.index]

                #grav
                self.vel_y += 1
                if self.vel_y > 10:
                    self.vel_y = 10
                dy += self.vel_y

                #check collision
                self.in_air = True
                for tile in world.tile_list:
                    #check x
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y,self.width, self.height ):
                        dx = 0
                    if self.rect.x <= 0:
                        dx = 1
                    if self.rect.x >= screen_w - tile_size:
                        self.rect.x = screen_w - tile_size

                    #check y
                    if self.rect.y <= 0 or self.rect.y >= screen_h:
                        dy = 1
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height ):
                        #check if below ground
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                        #check if above ground
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.in_air = False

                #enemy
                #if pygame.sprite.spritecollide(self, blob_group, False):
                #    gameover = -1
                    #gameover_fx.play()

                #lava
                #if pygame.sprite.spritecollide(self, lava_group, False):
                #    gameover = -1
                    #gameover_fx.play()
                #fall to death
                if self.rect.y >= 480:
                    gameover = -1
                
                #platforms
                for platform in platform_group:
                    #y
                    if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height ):
                        self.image = climb_img
                        #climb
                        dy = 0
                        #moving up when on a ladder
                        if key[pygame.K_UP]: 
                            dy -= 2
                        #moving down when on a ladder
                        if key[pygame.K_DOWN] : 
                            dy += 2

                #update rect
                self.rect.x += dx
                self.rect.y += dy
                if self.rect.bottom > screen_h:
                    self.rect.bottom = screen_h
                    dy = 0

                #animation
                if self.counter >= walk_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images_right):
                        self.index = 0
                    if self.direction == 1:
                        self.image = self.images_right[self.index]
                    if self.direction == -1:
                        self.image = self.images_left[self.index]
            
            elif gameover == -1:
                self.image = self.dead_image
                draw_text('GAME OVER!',font, blue, (screen_w //2) -200, screen_h //2 )
                if self.rect.y > 200:
                    self.rect.y -= 1
            screen.blit(self.image, self.rect)
            return gameover

        def reset(self, x, y):
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            for num in range(1,3):
                img_right = pygame.image.load(f'guy{num}.png')
                img_right = pygame.transform.scale(img_right, (tile_size,tile_size))
                img_left = pygame.transform.flip(img_right, True, False)
                self.images_right.append(img_right)
                self.images_left.append(img_left)
            self.dead_image = pygame.image.load('idle.png')
            self.image = self.images_right[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vel_y = 0
            self.jumped = False
            self.direction = 0
            self.in_air = True

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('climb.png')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.movedirection = 1
            self.movecounter = 0

        def update(self):
            self.rect.x += self.movedirection
            self.movecounter += 1
            if abs(self.movecounter) > 50:
                self.movedirection *= -1
                self.movecounter *= -1

    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
#            img = pygame.image.load('ladder.png')
            self.image = pygame.transform.scale(ladder_img, (tile_size, tile_size //2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.climb = True


        def update(self):
            pass

    class Lava(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('chain.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size //2))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('coin.png')
            self.image = pygame.transform.scale(img, (tile_size, int(tile_size )))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)

    class Exit(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load('climb.png')
            self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    class World():
        def __init__(self,data):
            self.tile_list = []
            row_count = 0
            for row in data:
                col_count = 0
                for tile in row:
                    if tile == 1: #block
                        img = pygame.transform.scale(block_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile= (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 2: #chain
                        platform = Platform(col_count * tile_size, row_count * tile_size)
                        platform.image = pygame.transform.scale(chain_img, (tile_size, tile_size))
                        platform_group.add(platform)
                    if tile == 3: #ladder left
                        platform = Platform(col_count * tile_size, row_count * tile_size)
                        platform.image = pygame.transform.scale(ladder_img, (tile_size, tile_size))
                        platform_group.add(platform)
                    if tile == 4: #ladder right
                        platform = Platform(col_count * tile_size, row_count * tile_size)
                        lad = pygame.transform.flip(ladder_img, True, False)
                        platform.image = pygame.transform.scale(lad, (tile_size, tile_size))
                        platform_group.add(platform)
                    if tile == 6:
                        lava = Lava(col_count * tile_size, row_count * tile_size)
                        #lava_group.add(lava)
                    if tile == 7:
                        coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                        coin_group.add(coin)
                    if tile == 8:
                        exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                        #exit_group.add(exit)
                    col_count +=1
                row_count +=1

        def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0], tile[1])
            print(tile[1])
    
    clock.tick(fps)
    screen.blit(bg_img, (0,0))

    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    world.draw()


    print(clock)
    exit_button = Buttons(screen_w //2 - 350, screen_h //2 -200, exit_img)
    if  exit_button.draw():
        game_run = False 
    player = Player(screen_w //2 , 430)
    if gameover == 0:
        #blob_group.update()
        #update score
        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
            if score % 2 == 0:
                gameover = 1

            #coin_fx.play()
        #display score
        screen.blit(bg_bottom, (0, screen_h-50))
        draw_text('Score: ' + str(score), font_score, white, tile_size - 10, screen_h - 50)

    #platform_group.draw(screen)
    #coin_group.draw(screen)
    gameover = player.update(gameover)

    if gameover == -1:
        game_run = False
        if restart_button.draw():
            world_data = []
            world = reset_level(level)
            gameover = 0
            score = 0
    
    if gameover == 1:
        level += 1 
        loaded = False
        if level <= max_levels:
            #reset level
            world_data = []
            world = reset_level(level)
            gameover = 0
        else:
            draw_text('YOU WIN!', font, blue,(screen_w //2) -140, screen_h //2  )
            #restart game
            if restart_button.draw():
                game=False
                main = True
                loaded = False
    
    pygame.display.update()
    return game_run


while run:
    main_menu()
    while game_run:
        game()
    pygame.display.update()

pygame.quit()