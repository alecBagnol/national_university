import sys
import cv2 as cv
import pygame

#inicia el entorno de pygame
pygame.init() 

#inicializando la pantalla al tamaño de un arreglo [ancho,alto]
screen = pygame.display.set_mode([640,448])
screen_w = screen.get_width()
screen_h = screen.get_height()
#le da nombre a la ventana
pygame.display.set_caption("Bricks") 


class Graphic:
    def __init__ (self, pic_path, ratio=1, pos=[0,0], key=[0,255,0],has_gravity=False):
        self.pic_path = pic_path
        self.ratio = ratio
        self.key = key
        self.pos = pos
        self.has_gravity = has_gravity
        self.is_jumping = False
        self.collision = False
        self.ammo = []

        self.frame_jump = 0
        self.time_e = 1

    def set_variables(self):
        self.velinit = 8
        self.vel = self.velinit
        self.mass = 0.5
        self.y_index = 1

    def img_topixel(self, cvimage, surface):
        for y, row in enumerate(cvimage):
            for x, col in enumerate(row):
                color_rgb = list(col)
                if color_rgb != self.key:
                    rect = pygame.Rect(x*self.ratio,y*self.ratio,self.ratio,self.ratio)
                    colour = (color_rgb[2],color_rgb[1],color_rgb[0])
                    surface.fill(colour, rect=rect)
        surface.set_colorkey([0,0,0])
    
    def img_std(self):
        self.img = cv.imread(self.pic_path)
        self.shape = self.img.shape
        self.w = self.shape[1] * self.ratio
        self.h = self.shape[0] * self.ratio
        self.surf = pygame.Surface((self.w, self.h))
        self.img_topixel(self.img, self.surf)

    def bounding(self):
# pygame tiene en su libreria deteccion de colisiones que para entenderla hay que pensar primero en que se está obviamente en un plano y que cada objeto tiene una posicion y un espacio dentro del canvas o superficie.
# las superficies usuales son dadas a partir del espacio enmarcado por un rectangulo, pero tambien se pueden dar superficies que se evaluan pixel a pixel.
# en el caso de ver si un rectangulo a colisiona con un rectangulo b se puede entender como:
# if a_x < b_x + b_ancho and a_x + a_ancho > b_x and a_y < b_y + b_alto and a_y + a_alto > b_y :
#     hay colisión!!!
        self.bounding_area = pygame.Rect(self.pos[0], self.pos[1], self.w, self.h)       

    def graphic_to(self, layer):
        layer.blit(self.surf, self.pos)

    def img_mov(self,axis, quantity):
        if axis == 'L':
            self.pos[0] -= quantity
        if axis == 'R':
            self.pos[0] += quantity
    
    def load_jump_animation(self, path):
        self.jump_img = cv.imread(path)
        self.jump_shape = self.jump_img.shape
        self.jump_w = self.jump_shape[1] * self.ratio
        self.jump_h = self.jump_shape[0] * self.ratio
        self.jump_surf = pygame.Surface((self.jump_w, self.jump_h))
        self.img_topixel(self.jump_img, self.jump_surf)

    def blink(self, surface):
        empty = pygame.Color(0,0,0,0)
        surface.fill(empty)

    def jump(self):
        if self.vel != 0:
            self.pos[1] -= (0.5*self.mass*(self.vel**2))*self.y_index
            self.vel -= 0.5
        else:
            self.is_jumping = False
        
    def animation_jump(self, count):
        self.blink(self.surf)
        self.jump_pos = [-self.w * count, 0]
        self.surf.blit(self.jump_surf, self.jump_pos)

    def initialize(self):
        self.set_variables()
        self.img_std()
        self.bounding()

    def load_rock(self, path):
        self.rock_img = cv.imread(path)
        self.rock_shape = self.rock_img.shape
        self.rock_w = self.rock_shape[1] * self.ratio
        self.rock_h = self.rock_shape[0] * self.ratio
        self.rock_surf = pygame.Surface((self.rock_w, self.rock_h))
        self.img_topixel(self.rock_img, self.rock_surf)
    
    def throw_rock(self, layer, coord):
        item = []
        new_s = pygame.Surface([16,16])
        new_s.blit(self.rock_surf, [0,0])
        new_s.convert_alpha()
        item.append(new_s)
        item.append(coord)
        self.ammo.append(item)
        layer.blit(self.ammo[len(self.ammo)-1][0], coord)
    

class Terrain:
    def __init__(self, ratio,windows_size):
        self.ratio = ratio
        self.win_w = windows_size[0]
        self.win_h = windows_size[1]
        self.map = [False]

    def tile(self, class_img):
        class_img.ratio = self.ratio
        class_img.set_variables()
        self.map.append(class_img)

    def start(self):
        for i, img in enumerate(self.map):
            if i != 0:
                img.initialize()

    def mapping(self, text_map, layer):
        self.boundings = []
        self.terra_map = text_map
        for y , row in enumerate(self.terra_map):
            pos_set = []
            for x, tile in enumerate(row):
                if tile != 0:
                    width = self.map[tile].w
                    height = self.map[tile].h
                    shape = [x*width, y*height, width, height]
                    pos_set.append(shape)

                    self.map[tile].pos[0] = shape[0]
                    self.map[tile].pos[1] = shape[1]
                    self.map[tile].graphic_to(layer)
                else:
                    pos_set.append([0,0,0,0])

            width = 0
            height = pos_set[0][3]
            for shape in pos_set:
                width += shape[2]
            rect = pygame.Rect(pos_set[0][0],pos_set[0][1],width,height)
            self.boundings.append(rect)
                        


    def collide_test(self, obj):
        truth = False
        for chunk in self.boundings:
            obj.bounding()
            test = obj.bounding_area.colliderect(chunk)
            truth = truth or test
        return truth

    def display(self, layer):
        for img in self.map:
            img.graphic_to(layer)

r = pygame.Color("red")
w = pygame.Color("white")
b = pygame.Color("blue")
black = pygame.Color("black")


hut = Graphic('pictures/hut.png',2,[-80,250],[0,255,0])
hut.initialize()
hut.pos = [-150, screen_h - hut.h - 6]

character = Graphic('pictures/Owl.png',2,[200,50],[0,0,0], True)
character.initialize()
character.load_jump_animation('pictures/Owl_jump.png')
character.load_rock('pictures/Rock1.png')

simple_terrain = Terrain(2, [screen_w, screen_h])
tile_sgs = Graphic('pictures/Tile_60.png')
tile_sss = Graphic('pictures/Tile_40.png')
tile_ggg = Graphic('pictures/Tile_02.png')
tile_ssg = Graphic('pictures/Tile_50.png')
tile_no = Graphic('pictures/transparent.png')

background = pygame.image.load('pictures/Background.png')
background = pygame.transform.scale(background,[640,448])

bloated = pygame.image.load('pictures/Big_bloated_walk.png')
bloated = pygame.transform.scale2x(bloated)
bloated_surf = pygame.Surface([144,144])


simple_terrain.tile(tile_sgs)
simple_terrain.tile(tile_sss)
simple_terrain.tile(tile_ssg)
simple_terrain.tile(tile_ggg)
simple_terrain.tile(tile_no)

simple_terrain.start()

data = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 5, 5, 5, 0, 0, 0, 0, 0, 0, 0 ],
    [ 2, 2, 2, 3, 4, 4, 4, 4, 4, 4 ],
]


L_move = False
R_move = False
U_move = False



test_rect = pygame.Rect(100,100,100,50)

def move_action(w,x,z):
        if L_move:
            character.img_mov('L', w)
        if R_move:
            character.img_mov('R', x)
        if U_move:
            character.is_jumping = True
    

def throwing():
    coord = coorde()
    new_s = pygame.Surface([16,16])
    new_s.blit(character.rock_surf, [0,0])
    character.ammo.append([new_s,coord])
    screen.blit(character.ammo[len(character.ammo)-1][0], coord)


def coorde():
    x_char = character.pos[0] + 32
    y_char = character.pos[1] + 32
    return [x_char, y_char]

jump_around = False
clock = pygame.time.Clock()
jump_counter = 0

throw_rock = False
rock_counter = 0

tic = 1
xfact = 1
x_blot = 0

while True:
    clock.tick(60) #fps
    screen.fill(b) #elimina el trail de la imagen cargada
    screen.blit(background,[0,0])
    simple_terrain.mapping(data,screen)
    hut.graphic_to(screen)
    bloated_surf.fill([0,0,0,0])
    bloated_surf.blit(bloated, [-xfact,0])
    bloated_surf.set_colorkey([0,0,0])
    screen.blit(bloated_surf, [900-x_blot,245])

    character.graphic_to(screen)
    tic += 1
    if tic % 10 == 0:
        xfact += 144
        x_blot += 6
    if tic == 60:
        tic = 0
        xfact = 0
    if x_blot > 750:
        x_blot -= 6 


    if jump_around:
        character.jump()
        frame_counter = jump_counter//5

        if frame_counter > 7:
                frame_counter = 0
                jump_counter = 0
                jump_around = False

        if jump_counter % 5 == 0:
            character.animation_jump(frame_counter)
        jump_counter += 1

    
    for i, rock in enumerate(character.ammo):
        rock[1][0] += 10
        # rock[1][1] += 5
        if rock[1][1] > (448-64):
            character.ammo.pop(i)
        screen.blit(rock[0], rock[1])


    if simple_terrain.collide_test(character):
        # pygame.draw.rect(screen,r,test_rect)
        character.collision = True
        move_action(4,4,0)
    else:
        # pygame.draw.rect(screen,b,test_rect)
        move_action(4,4,4)
        character.collision = False

    if not character.collision and not character.is_jumping:
        if character.vel != character.velinit:
            character.vel += 0.5
        else:
            character.is_jumping = False
        
        character.pos[1] += (0.5*character.mass*(character.vel**2))*character.y_index

    elif character.collision and not character.is_jumping:
        character.vel = character.velinit

    for event in pygame.event.get(): #loop de eventos
        if event.type == pygame.QUIT: #evento de cierre de ventana
            pygame.quit() #primero para pygame
            sys.exit() #detiene el script

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                R_move = True
            if event.key == pygame.K_LEFT:
                L_move = True
            if event.key == pygame.K_UP:
                
                if jump_around:
                    U_move = False
                else:
                    U_move = True
                    jump_around = True
            if event.key == pygame.K_SPACE:
                throwing()

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                R_move = False
            if event.key == pygame.K_LEFT:
                L_move = False
            if event.key == pygame.K_UP:
                U_move = False

    
    pygame.display.update() #actualizar el display, no se actualiza hasta que no se llama este metodo
    

