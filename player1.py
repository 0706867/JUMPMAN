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
gameover = 0
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
                gameover = -1
                #gameover_fx.play()
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
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 10
        self.dy = 10
        self.direction = 1

    def update(self):
        rotated = False
        player_detectedy = False
        player_detectedx = False
        detected = False
        if self.direction == 0: #move horizontally
            self.rect.x += self.dx
            if self.rect.x >= screen_w:
                self.direction = 1
                self.rect.y = 0
                self.rect.x = randint(0,screen_w-30)
                rotated = True
            if self.rect.x <= player_pos.x:
                while not detected:
                    if self.rect.y+tile_size >= player_pos.y and self.rect.y +tile_size<= player_pos.y+tile_size:
                        player_detectedy = True
                        detected = True
                        print("selfy: " + str(self.rect.y) +"playery: " + str(player_pos.y))
            if player_detectedy:
                if self.rect.x <= screen_w:
                    self.dx = 20
            else:
                self.dx = 2
        
        if self.direction == 1: #move vertically
            self.rect.y += self.dy
            if self.rect.y >= screen_h- 150:
                self.direction = 0
                self.rect.x = 0
                #self.rect.y = randint(0,screen_h-180)
                self.rect.y = 400
                rotated = True
                
            
            
            if self.rect.y <= player_pos.y:
                #while detected == False:
                if self.rect.x+tile_size >= player_pos.x and self.rect.x +tile_size<= player_pos.x+tile_size:
                    player_detectedx = True
                    print("selfy: " + str(self.rect.x) +"playery: " + str(player_pos.x))
            if player_detectedx:
                self.dy = 20
            else:
                self.dy = 2

#rotate based on direction
        if rotated:
            if self.direction == 0: #rotate horizontally
                self.image = pygame.transform.rotate(self.image, 90)
                rotated = False
            if self.direction == 1: #rotate vertically
                self.image = pygame.transform.rotate(self.image, -90)
                rotated = False
        
        
        

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

    def update(self):
        self.rect.x += self.movedirection
        self.movecounter += 1
        if abs(self.movecounter) > 50:
            self.movedirection *= -1
            self.movecounter *= -1

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
bullet = Enemy1(randint(0,screen_w-30),randint(0,screen_h-180))
bullet_group.add(bullet)
#blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
#exit_group = pygame.sprite.Group()
score_coin = Coin(tile_size //2, tile_size //2)
#coin_group.add(score_coin)
restart_button = Buttons(screen_w //2 - 50, screen_h //2 + 100, restart_img)
exit_button = Buttons(screen_w //2 - 350, screen_h //2 , exit_img)
start_button = Buttons(screen_w //2 + 150, screen_h //2, start_img)
solo_button = Buttons(screen_w //2 + 150, screen_h //2, singleplayer_img)
multi_button = Buttons(screen_w //2 - 350, screen_h //2, versus_img)

run = True #is game running - used for closing game
loaded = False #is map loaded - used for reskinning code
multiple = False
solo = False
game = False
run_game = False

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
#if the current scene is the main menu
    if main:
#draw and exit and start button, when pressed exit, exits the game and start, stop the menu scene and start games scene
        if exit_button.draw():
            run = False
        if start_button.draw():
            main = False
            game = True 
    if game:
        #reset game variables
        level = 1
        score = 0
        world_data = []
        world_loaded[0] = reset_level(level)
        gameover = 0

        if solo_button.draw():
            game = False
            solo = True
        if multi_button.draw():
            game = False
            multiple = True

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
                enemy.enemy3()
#update score
            if pygame.sprite.spritecollide(player, coin_group, True): #if player collides with coin, score goes up
                score += 1
                if len(coin_group) == score_to_pass: #if score is divisible by 2 and provides a whole number answer, player can pass the level
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
            if restart_button.draw(): #draw the restart button, when pressed reset the game variables
                world_data = []
                world_loaded[0] = reset_level(level)
                gameover = 0
                score = 0
                
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
                if restart_button.draw():
                    
                    main = True
                    game = False
                    run_game = False
                    solo = False 
                    multiple = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #if event.type == JOYDEVICEADDED:
        #    print("NEW DEVICE")

    
    pygame.display.update()


#when game is not running
pygame.quit()