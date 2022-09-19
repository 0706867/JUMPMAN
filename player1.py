from random import random
from random import randint
import pygame
import os
import platform
from pygame import Vector2, mixer
import pickle
from os import path
import socket
import threading

#audio set up
pygame.mixer.pre_init(44100, -16, 2, 512)

mixer.init()
pygame.init()

#if ran on the retro pi initailise the buttons

#if os.uname().nodename == 'raspberrypi':
if platform.system() == 'raspberrypi':
    from gpiozero import Button
    #joystick buttons
    joystick_up = Button(4)
    joystick_down = Button(17)
    joystick_left = Button(27)
    joystick_right = Button(22)
    button_top_left = Button(18)
    button_top_middle = Button(15)
    button_top_right = Button(14)
    button_bottom_left = Button(25)
    button_bottom_middle = Button(24)
    button_bottom_right = Button(23)
    button_blue_left = Button(10)
    button_blue_right = Button(9)

clock = pygame.time.Clock()
fps = 60

screen_w = 960
screen_h = 600

#font
font_score = pygame.font.SysFont('Arial', 50)
font = pygame.font.SysFont('Arial', 70)

#variables
tile_size = 24
gameover = -1
main = True
level = 1
max_levels = 3
score = 0
theme = 0
world_loaded = []
player_pos = Vector2(int(0),int(0))
score_to_pass = 10

#colours
white = (255,255,255)
blue = (0,0,200)

#screen setup
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Server')

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
singleplayer_img = pygame.image.load('singleplayer.png')
singleplayer_img = pygame.transform.scale(singleplayer_img, (120, 120))
versus_img = pygame.image.load('versus.png')
versus_img = pygame.transform.scale(versus_img, (120, 120))

#default theme
level_1_alt = ['bg.png', 'block2.png', 'ladder.png']

#level 1    background image            block image             ladder image
level_1 = ['level 1/ice_bg.png', 'level 1/ice_block.png','level 1/ice_ladder_clear.png']

#level 2    background image            block image             ladder image
level_2 = ['level 2/hall_bg.png', 'level 2/hall_block.png','level 2/hall_ladder1.png','level 2/hall_ladder2.png', 'level 2/hall_ladder3.png']

#level 3    background image            block image             ladder image
level_3 = ['level 3/desert_bg.png', 'level 3/desert_block.png', 'level 3/desert_ladder.png']

#level 4    background image            character face             character death face     character idle image
level_4 = ['level 4/final_bg.png', 'level 4/luke_face.png', 'level 4/luke_death.png', 'level 4/luke_idle.png',
#enemy idle     enemy idle animation 2  enemy bullet        enemy death face            enemy face              enemy shoot anim
'enemy/enemy.png','enemy/enemy2.png', 'enemy/bullet.png','enemy/enemy_death.png', 'enemy/enemy_face.png', 'enemy/enemy_shoot.png']

#audomatic images change
levels = [level_1, level_2, level_3, level_4]
#gets the index (current level-1 as array start at 0) from array above and select the required image
bg_img = pygame.image.load(levels[level-1] [0])
bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h-120))
block_img = pygame.image.load(levels[level-1] [1])
block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
ladder_img = pygame.image.load(levels[level-1] [2]) 
bg_bottom = pygame.image.load('bg.png')
bg_bottom = pygame.transform.scale(bg_bottom, (screen_w,screen_h))


#if theme is 1 load the sprites based on the level - star wars theme
if theme == 1:
    if level <= max_levels:
        bg_img = pygame.image.load(levels[level-1][0])
        bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h-120))
        block_img = pygame.image.load(levels[level-1][1])
        block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
        ladder_img = pygame.image.load(levels[level-1][2])
#if theme is 0 load the default sprites - original theme
if theme == 0:
    if level <= max_levels:
        bg_img = pygame.image.load('bg.png')
        bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h-120))
        block_img = pygame.image.load('block2.png')
        block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
        ladder_img = pygame.image.load('ladder.png') 
#sounds
#pygame.mixer.music.load('')
#pygame.mixer.music.play(-1, 0.0, 1000)
#coin_fx = pygame.mixer.Sound('')
#coin_fx.set_volume(0.5)
#jump_fx = pygame.mixer.Sound('')
#jump_fx.set_volume(0.5)
#gameover_fx = pygame.mixer.Sound('')
#gameover_fx.set_volume(0.5)

#converts text to image as required by pygame
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#reset current level
def reset_level(level):
    player.reset(screen_w //2 , 400)
#    player2.reset(screen_w //2 , 400)
    #blob_group.empty()
    robot_group.empty()
    #exit_group.empty()
    platform_group.empty()
    coin_group.empty()
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)
    world_loaded = [world]
    return world

#Multiplayer
class multi():
    def host_game(self, host, port):
        global multiple
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(10)

        client, addr = server.accept()
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        while run:
            text = str(player_pos)
            client.send(text.encode('utf-8'))
            data = client.recv(1024)
            if not data:
                break
            else:
                datas = data.decode('utf-8')
                if datas[2] >= str(0):
                    datas1 = datas[1] 
                    datas2 = datas[2] 
                    datas3 = datas[3] 
                    datas4 = datas[4] 
                    datas5 = datas[5] 
                    datas6 = datas[6] 
                    datas7 = datas[7]
                    datas8 = datas[8] 
                    #       01234567
                    #len 8  [0, 000]
                    #       012345678
                    #len 9  [00, 000]
                    #       0123456789
                    #len 10 [000, 000]
                    datasx = 2
                    datasy = 2
                    if len(datas) == 10:
                        datasx = int(str(datas1)+str(datas2)+str(datas3))
                        datasy = int(datas6+datas7+datas8)
                    if len(datas) == 9:
                        datasx = int(str(datas1)+str(datas2))
                        datasy = int(datas5+datas6+datas7)
                    if len(datas) == 8:
                        datasx = int(str(datas1))
                        datasy = int(datas4+datas5+datas6)
                    global coin_group
                    global player2
                    global score
                    global gameover
                    global score_to_pass
                    #print(text + " player 1")
                    #print(str(datas[7]))
                    player2 = Player2(datasx,datasy)
                    player2.update()
                    if pygame.sprite.spritecollide(player2, coin_group, True): #if player collides with coin, score goes up
                        score += 1      
                        if len(coin_group) == score_to_pass: #if score is divisible by 2 and provides a whole number answer, player can pass the level
                            gameover = 1  
        client.close()
        return data


class Buttons():
    def __init__(self, x, y, image, button, tag):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.button = button
        self.tag = tag

    def draw(self):
        key = pygame.key.get_pressed()
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                self.clicked = True
        if key[self.button] and self.tag == button_options[current_selection]:
            action = True
            self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action

class Player():
    def __init__(self, x, y, up, down, left, right, jump):
        self.reset(x,y)
        self.up = up
        self.down = down
        self.left = left
        self.right = right 
        self.jump = jump


    def update(self, gameover):
        dx = 0
        dy = 0
        global player_pos 
        walk_cooldown = 5
        col_thresh = 20
        key = pygame.key.get_pressed()
        if gameover == 0:
            #play when keyboard is connected
            if (key[self.jump]) and self.jumped == False and self.in_air == False: #if space is pressed and player is not in air or jumping, let them jump
                #jump_fx.play()
                self.jumped = True
                self.vel_y = -10
            if (key[self.jump]) == False: #if player is not pressing space, dont jump
                self.jumped = False
            if key[self.left]: #when left key is pressed
                dx -= 2 #moves the player left and is used for collision - checks 2 pixels ahead
                self.counter += 1 #used for animation
                self.direction = -1 #used for animation
            if key[self.right] :
                dx += 2#moves the player left and is used for collision - checks 2 pixels ahead
                self.counter += 1#used for animation
                self.direction = 1#used for animation
            if key[self.left] == False and key[self.right] == False:#when left and right are not pressed
                self.counter = 0 #stops on current image
                self.index = 0 #used for animation
                if self.direction == 1: #if direction is 1, use right facing images
                    self.image = self.images_right[self.index]
                if self.direction == -1:  #if direction is -1, use left facing images
                    self.image = self.images_left[self.index]
            
            #only run when playing on the retro pi, same as above
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
            self.vel_y += 1 #always falling down - how fast you fall down
            if self.vel_y > 10: #max fall speed
                self.vel_y = 10
            dy += self.vel_y #fall down

            #check collision
            self.in_air = True #if player is in air - falling or jumping
            for tile in world_loaded[0].tile_list:
            #check x
                if tile[1].colliderect(self.rect.x + dx, self.rect.y,self.width, self.height ): #if player collides with walking blocks,stop moving
                    dx = 0
            #stop player from moving off screen
                if player_pos.x <= 0: 
                    dx = 1
                if player_pos.x >= screen_w - tile_size:
                    player_pos.x = screen_w - tile_size

            #check y
                if player_pos.y <= 0 or player_pos.y >= screen_h: #stop player from moving off screen
                    dy = 1
                if tile[1].colliderect(player_pos.x, player_pos.y + dy,self.width, self.height ):#if player collides with walking blocks
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
            #robot
            if pygame.sprite.spritecollide(self, robot_group, False):
                pass
#                gameover = -1
                #gameover_fx.play()
            #bullet
            if pygame.sprite.spritecollide(self, bullet_group, False):
                gameover = -1
            #fall to death
            if self.rect.y >= 480: #minimum y value - when the player falls off map
                gameover = -1  #player dies
            
#ladders
            for platform in platform_group:
                #when colliding with ladders, player images changes to 'climb.png' and player doesnt fall, up and down can be used to move
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height ):
                    self.image = climb_img
                    #climb
                    dy = 0
                    #moving up when on a ladder
                    if key[self.up]: 
                            dy -= 2
                    #moving down when on a ladder
                    if key[self.down] : 
                            dy += 2

#move the player
            self.rect.x += dx
            self.rect.y += dy
            player_pos = Vector2(self.rect.x, self.rect.y)
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
        
        elif gameover == -1: #when player is dead, update image to dead, draw 'Game Over' text
            self.image = self.dead_image
            draw_text('GAME OVER!',font, blue, (screen_w //2) -200, screen_h //2 )
            if self.rect.y > 200: #mini animation - player becomes smaller and floats up - like a ghost
                self.rect.y -= 1
        screen.blit(self.image, self.rect)
        return gameover

    def reset(self, x, y): #reset variables
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

class Player2():
    def __init__(self, x, y):
        self.reset(x,y)

    def update(self):
        global player_pos 
        screen.blit(self.image, self.rect)

    def reset(self, x, y): #reset variables
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
                if tile == 5:
                    robot = Enemy2(col_count * tile_size, row_count * tile_size)
                    robot_group.add(robot)
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

#bullet
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy/bullet.png')
        self.image = pygame.transform.scale(self.image, (tile_size//2, tile_size//2))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.speed = 2 #base speed
        self.fastspeed = 5 #increased speed
        self.rect.x = x 
        self.rect.y = y
        self.dx = 10
        self.dy = 10
        self.direction = 1 #vertical = 1, horizontal  = 0
        self.detected = False #if the player has been detected
        self.bullet_is_behind = False #is the bullet behind
        self.bullet_is_ahead = False #is the bullet ahead
        self.bullet_is_above = False #is the bullet above
        self.bullet_is_below = False #is the bullet below

    def update(self):
        rotated = False #has the image been rotated
    #reset bullet
        #if the bullet goes outside the screen - left or right
        if self.rect.x >= screen_w-20 or self.rect.x <= 0:
            self.image = pygame.transform.rotate(self.image, 90)    #rotate image
            self.direction = 1                                      #change direction to vertical
                                                                    #reset bullet position variables
            self.bullet_is_ahead = False
            self.bullet_is_below = False
            self.bullet_is_behind = False
            self.bullet_is_above = False
            self.detected = False                                   #player has not been detected
        #if the player went out the right side
            if self.rect.x >= screen_w-20:
                #print('went out the right side')
                #set the bullet starting position to y = 10 and move the bullet down
                self.rect.y = 10
                self.rect.x = randint(50,screen_w-50)
                self.dy = self.speed
        #if the player went out the left side
            if self.rect.x <= 0:
                #print('went out the left side')
                #set the bullet starting position to y = 10 and move the bullet down
                self.rect.y = 10
                self.rect.x = randint(50,screen_w-50)
                self.dy = self.speed
        #if the bullet goes outside the screen - up and down
        if self.rect.y >= screen_h-180 or self.rect.y <= 0:
            self.image = pygame.transform.rotate(self.image, -90)   #rotate image
            self.direction = 0                                      #change direction to horizontal
                                                                    #reset bullet position variables
            self.bullet_is_ahead = False
            self.bullet_is_below = False
            self.bullet_is_behind = False
            self.bullet_is_above = False
            self.detected = False                                   #player has not been detected
        #if the player went out the from the bottom side
            if self.rect.y >= screen_h-180:
                #print('went out the bottom')
                #set the bullet starting position to x = end of the screen and move the bullet backward
                self.rect.y = randint(50,screen_h-200)
                self.rect.x = screen_w-20
                self.dx = -self.speed
         #if the player went out the from the top
            if self.rect.y <= 0:
                #print('went out the top')
                #set the bullet starting position to x = 10 and move the bullet forward
                self.rect.y = randint(50,screen_h-200)
                self.rect.x = 10
                self.dx = self.speed
    #if moving horizontally
        if self.direction == 0:
            self.dy = 0
            self.rect.x += self.dx
            self.rect.y += self.dy
            
    #if moving vertically
        if self.direction == 1:
            self.dx = 0
            self.rect.y += self.dy
            self.rect.x += self.dx

#if the player has not been detected
        if self.detected == False:
    #check y
            if (self.rect.x+tile_size//2) >= (player_pos.x) and (self.rect.x +tile_size//2)<= (player_pos.x+tile_size//2):
                #rotate image
                self.image = pygame.transform.rotate(self.image, -90)
                #if the bullet's y is greater than the player's y
                if self.rect.y >= player_pos.y:
#                    print('below')
                    self.bullet_is_below = True
                    self.bullet_is_above = False
                    self.detected = True
                #if the bullet's y is less than the player's y
                if self.rect.y <= player_pos.y:
#                    print('above')
                    self.bullet_is_above = True
                    self.bullet_is_below = False
                    self.detected = True
    #check x
            if (self.rect.y+tile_size//2) >= (player_pos.y) and (self.rect.y +tile_size//2)<= (player_pos.y+tile_size//2):
                self.image = pygame.transform.rotate(self.image, 90)
                #if the bullet's x is greater than the player's x
                if self.rect.x >= player_pos.x:
#                    print('ahead')
                    self.bullet_is_ahead = True
                    self.bullet_is_behind = False
                    self.detected = True
                #if the bullet's x is greater than the player's x
                if self.rect.x <= player_pos.x:
#                    print('behind')
                    self.bullet_is_behind = True
                    self.bullet_is_ahead = False
                    self.detected = True

    #if player is detected move bullet faster   
        #if the bullet is behind the player
        if self.bullet_is_behind:
            #if the bullet's x is less than the end of the screen increase the speed
           if self.rect.x <= screen_w:
#                print('behind2')
                self.dx = self.fastspeed
                self.dy = 0
                self.rect.y += self.dy
                self.rect.x += self.dx

        #if the bullet is ahead of the player
        if self.bullet_is_ahead:
            #if the bullet's x is greater than the start of the screen increase the speed
            if self.rect.x >= 0:
#                print('ahead2')
                self.dx = -self.fastspeed
                self.dy = 0
                self.rect.y += self.dy
                self.rect.x += self.dx

        #if the bullet is above the player
        if self.bullet_is_above:
            #if the bullet's y is less than the end of the screen increase the speed
            if self.rect.y <= screen_h-150:
#                print('above2')
                self.dy = self.fastspeed
                self.dx = 0
                self.rect.y += self.dy
                self.rect.x += self.dx
        #if the bullet is below the player
        if self.bullet_is_below:
            #if the bullet's y is greater than the start of the screen increase the speed
            if self.rect.y >= 0:
#                print('below2')
                self.dy = -self.fastspeed
                self.dx = 0
                self.rect.y += self.dy
                self.rect.x += self.dx

#pac man ghosts
class Enemy2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy/enemy_face.png')
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movedirection = 1
        self.movecounter = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.in_air = True
        self.i = 0
        self.touch = False

    def update(self):
        dx = 2
        dy = 0
        pos = pygame.mouse.get_pos()
        #self.rect.x = pos[0]
        #self.rect.y = pos[1]

        #grav
        self.vel_y += 1 #always falling down - how fast you fall down
        if self.vel_y > 10: #max fall speed
            self.vel_y = 10
        dy += self.vel_y #fall down
        #check collision
        self.in_air = True #if player is in air - falling or jumping
        for tile in world_loaded[0].tile_list:
            
            if self.rect.y+25 >= tile[1].y and self.rect.y +35 <= tile[1].y+40 and self.rect.x+10 >= tile[1].x and self.rect.x+10 <= tile[1].x+40:
                self.touch = True
                #print(tile[1].x)
                print('floor')
            ####################################################
            #else breaks the code - need to rewrite/rethink the else statement
            else:
                self.touch = False
            if not self.touch:
                self.i += 1
                print('no floor' + str(self.i))
                #print(str(self.rect.x) +","+ str(self.rect.y))
            pygame.draw.rect(screen, (255), (self.rect.x, self.rect.y+25, self.width,10))
            #print(touch)
        #check x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y,self.width, self.height ): #if player collides with walking blocks,stop moving
                dx = 0
        #stop player from moving off screen
            if self.rect.x <= 0: 
                dx = 1
            if self.rect.x >= screen_w - tile_size:
                self.rect.x = screen_w - tile_size

        #check y
            if self.rect.y <= 0 or self.rect.y >= screen_h: #stop player from moving off screen
                dy = 1
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width, self.height ):#if player collides with walking blocks
                if self.rect.x >= screen_w - 20:
                    self.rect.x += dx
                elif self.rect.x <= 20:
                    self.rect.x -= dx
                    
                #check if below ground
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above ground
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
            
        
#ladders
        for platform in platform_group:
            #when colliding with ladders, player images changes to 'climb.png' and player doesnt fall, up and down can be used to move
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height ):
                #climb
                dy = 0
                

#move the player
        self.rect.x += dx
        self.rect.y += dy
        
        screen.blit(self.image, self.rect)
        
        #if abs(self.movecounter) > 50:
        #    self.movedirection *= -1
        #    self.movecounter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('ladder.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size //2))
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

world_data = []
key = pygame.key.get_pressed()
player = Player(screen_w //2 , 430,  pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE)
#player2 = Player(screen_w //3 , 430, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_o)
robot_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
bullet = Enemy1(20,50)
#blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
#exit_group = pygame.sprite.Group()
score_coin = Coin(tile_size //2, tile_size //2)
#coin_group.add(score_coin)
restart_button = Buttons(screen_w //2 - 50, screen_h //2 + 100, restart_img, pygame.K_k, "restart")
exit_button = Buttons(screen_w //2 - 350, screen_h //2 , exit_img, pygame.K_k, "exit")
start_button = Buttons(screen_w //2 + 150, screen_h //2, start_img, pygame.K_k, "start")
solo_button = Buttons(screen_w //2 + 150, screen_h //2, singleplayer_img, pygame.K_k, "solo")
multi_button = Buttons(screen_w //2 - 350, screen_h //2, versus_img, pygame.K_k, "multi")

run = True #is game running - used for closing game
loaded = False #is map loaded - used for reskinning code
multiple = False
solo = False
game = False
run_game = False

button_selected_start = False
button_selected_option = False
button_selected_exit = False
button_selected_solo = False
button_selected_multi = False
button_selected_back = False
button_selected_restart = False
current_selection = 3
button_options = {1: "exit" , 2: "options", 3: "start",4:" ", 5:"solo", 6:"multi", 7:"back", 8:" ",  9: "restart", 10: " " }

while run: #while game is running
    clock.tick(fps)
    screen.blit(bg_img, (0,0))
    world_drawn = 0
# if world not loaded, get the map based on level nnumber from the file and set the data inside "world" variable and set "loaded" to true
    if not loaded:
        if path.exists(f'level{level}_data'):
            pickle_in = open(f'level{level}_data', 'rb')
            world_data = pickle.load(pickle_in)
        world = World(world_data)
        world_loaded = [world]
        loaded = True
    
#if theme is 1 load the sprites based on the level - star wars theme
    if theme == 1:
        if level <= max_levels:
            bg_img = pygame.image.load(levels[level-1][0])
            bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h-120))
            block_img = pygame.image.load(levels[level-1][1])
            block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
            ladder_img = pygame.image.load(levels[level-1][2])
#if theme is 0 load the default sprites - original theme
    if theme == 0:
        if level <= max_levels:
            bg_img = pygame.image.load('bg.png')
            bg_img = pygame.transform.scale(bg_img, (screen_w,screen_h-120))
            block_img = pygame.image.load('block2.png')
            block_img = pygame.transform.scale(block_img, (tile_size,tile_size))
            ladder_img = pygame.image.load('ladder.png') 
#(if 4 is pressed set theme to 0, if 5 is pressed set theme to 1) and reload the world.
    if pygame.key.get_pressed()[pygame.K_4]:
        theme = 0
        loaded = False
    if pygame.key.get_pressed()[pygame.K_5]:
        theme = 1
        loaded = False

#used for selecting with keyboard
    #if currently selected is 1, button is exit and so on....
    if current_selection == 1:
        button_selected_exit = True
    else:
        button_selected_exit = False

    if current_selection == 2:
        button_selected_option = True
    else:
        button_selected_option = False

    if current_selection== 3 :
        button_selected_start = True
    else:
        button_selected_start = False

    if current_selection == 5:
        button_selected_solo = True
    else:
        button_selected_solo = False

    if current_selection == 6:
        button_selected_multi = True
    else:
        button_selected_multi = False

    if current_selection== 7:
        button_selected_back = True
    else:
        button_selected_back = False

    if current_selection== 9:
        button_selected_restart = True
    else:
        button_selected_restart = False

#if layer is on the satrtup screen
    if main:
        #if the button is currently selected, draw its border
        if button_selected_start:
            pygame.draw.rect(screen, (140,140,140), (screen_w //2 + 130, screen_h //2-20, 320, 160))
        
        if button_selected_exit:
            pygame.draw.rect(screen, (140,140,140), (screen_w //2 - 370, screen_h //2-20, 280, 160))
        #allows the selection to loop from left to right or right to left
        if current_selection <= 0: #blank
            current_selection = 3 #start
        #if the player is past 4 go to 1, if the player just restarted go to 1
        if current_selection >= 4 and current_selection <= 6 or current_selection >= 10: #ahead of blank and less than multi or greater than blank
            current_selection = 1#exit
#draw exit and start buttons, when pressed exit, exits the game and start, stop the menu scene and start games scene
        if exit_button.draw():
            run = False
        
        if start_button.draw():
            main = False
            game = True 
            current_selection = 4
#if player is on the gamemode selection screen
    if game:
        #if the button is currently selected, draw its border
        if button_selected_multi:
            pygame.draw.rect(screen, (140,140,140), (screen_w //2 -360, screen_h //2-20, 150, 160))
        if button_selected_solo:
            pygame.draw.rect(screen, (140,140,140), (screen_w //2 + 130, screen_h //2-20, 160, 160))

        #allows the selection to loop from left to right or right to left
        if current_selection <= 4: #blank
            current_selection = 7 #back
        if current_selection >= 8: #blank
            current_selection = 5 #solo
        #reset game variables
        level = 2
        score = 0
        world_data = []
        world_loaded[0] = reset_level(level)
        #delete and create bullet for level 1
        bullet_group.empty()
        bullet = Enemy1(20,50)
        bullet_group.add(bullet)

        if solo_button.draw():
            game = False
            solo = True
            gameover = 0

        if multi_button.draw():
            game = False
            multiple = True
            gameover = 0

        if multiple:
            multi().host_game('localhost', 9999)
            run_game = True

        if solo:
            run_game = True
    
    if run_game and loaded:
        loaded = True
        if len(world_loaded) <= 5:
            world_loaded[0].draw()
            world_drawn += 1
        if world_drawn >= 5:
            world_loaded.pop()

#if game is running
        if gameover == 0:
            platform_group.draw(screen)
            coin_group.draw(screen)
#display different enemy based on the level
            if level == 1:
                bullet_group.update()
                bullet_group.draw(screen)
            if level == 2:
                robot_group.update()
                robot_group.draw(screen)
            if level == 3:
                enemy = Enemy2(240,40)
                
#update score
            if pygame.sprite.spritecollide(player, coin_group, True): #if player collides with coin, score goes up
                score += 1
                if len(coin_group) == score_to_pass: #if teh size of coin group is the same as the required amount to pass
                    gameover = 1
                #coin_fx.play()
#display score
            screen.blit(bg_bottom, (0, screen_h-50))
            draw_text('Score: ' + str(score), font_score, white, tile_size - 10, screen_h - 50)


        #blob_group.draw(screen)
        gameover = player.update(gameover)
#        gameover = player2.update(gameover)
#if player dies
        if gameover == -1:
            current_selection = 9 #blank
            if button_selected_restart:
                pygame.draw.rect(screen, (140,140,140), (screen_w //2 - 60, screen_h //2 + 90, 140, 60))
            if restart_button.draw(): #draw the restart button, when pressed reset the game variables
                world_data = []
                world_loaded[0] = reset_level(level)
                score = 0
                main = True
                game = False
                run_game = False
                solo = False 
                multiple = False
                

                
#if player passes level
        if gameover == 1: #next level starts and the world is not loaded
            level += 1 
            loaded = False
            
            if level <= max_levels: #when level number is lower than total levels, resets levels
                world_data = []
                world_loaded[0] = reset_level(level)
                gameover = 0
                coin_group.empty()
            else: #if player finishes last level, display text and reset game
                draw_text('YOU WIN!', font, blue,(screen_w //2) -140, screen_h //2  )
                #restart game
                current_selection = 9 #blank
                if button_selected_restart:
                    pygame.draw.rect(screen, (140,140,140), (screen_w //2 - 60, screen_h //2 + 90, 140, 60))
                if restart_button.draw():
                    main = True
                    game = False
                    run_game = False
                    solo = False 
                    multiple = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #if game is not being played, allow user to select buttons
        if gameover != 0:
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    current_selection -=1
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    current_selection +=1

        #if event.type == JOYDEVICEADDED:
        #    print("NEW DEVICE")

    
    pygame.display.update()


#when game is not running
pygame.quit()