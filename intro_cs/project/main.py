import sys
import cv2 as cv
import pygame
# pygame tiene en su libreria deteccion de colisiones que para entenderla hay que pensar primero en que se está obviamente en un plano y que cada objeto tiene una posicion y un espacio dentro del canvas o superficie.
# las superficies usuales son dadas a partir del espacio enmarcado por un rectangulo, pero tambien se pueden dar superficies que se evaluan pixel a pixel.
# en el caso de ver si un rectangulo a colisiona con un rectangulo b se puede entender como:
# if a_x < b_x + b_ancho and a_x + a_ancho > b_x and a_y < b_y + b_alto and a_y + a_alto > b_y :
#     hay colisión!!!


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
        self.img = cv.imread(self.pic_path)
        self.ratio = ratio
        self.key = key
        self.pos = pos
        self.has_gravity = has_gravity
        self.is_jumping = False
        self.collision = False

    def set_variables(self):
        self.velinit = 8
        self.vel = self.velinit
        self.mass = 0.5
        self.y_index = 1
        self.shape = self.img.shape
        self.w = self.shape[1] * self.ratio
        self.h = self.shape[0] * self.ratio
        self.surf = pygame.Surface((self.w, self.h))

    def img_topixel(self):
        for y, row in enumerate(self.img):
            for x, col in enumerate(row):
                color_rgb = list(col)
                if color_rgb != self.key:
                    rect = pygame.Rect(x*self.ratio,y*self.ratio,self.ratio,self.ratio)
                    colour = (color_rgb[2],color_rgb[1],color_rgb[0])
                    self.surf.fill(colour, rect=rect)
        self.surf.set_colorkey([0,0,0])

    def bounding(self):
        self.bounding_area = pygame.Rect(self.pos[0], self.pos[1], self.w, self.h)       

    def graphic_to(self, layer):
        self.jump()
        layer.blit(self.surf, self.pos)

    def img_mov(self,axis, quantity):
        if axis == 'L':
            self.pos[0] -= quantity
        if axis == 'R':
            self.pos[0] += quantity
        if axis == 'D':
            self.pos[1] += quantity
    
    def jump(self):
        if self.is_jumping:
            if self.vel != 0:
                # if self.y_index == -1 and self.collision:
                #     self.is_jumping = False
                #     self.y_index = 1
                #     self.vel = self.velinit
                # else:
                self.pos[1] -= (0.5*self.mass*(self.vel**2))*self.y_index
                self.vel -= 0.5
                
                
            # elif self.vel != self.velinit and self.y_index == 1:
                # self.y_index = -1
                # self.vel = self.velinit
            else:
                self.is_jumping = False
                # self.y_index = 1
                # self.vel = self.velinit
            

    def reset(self):
        pass

    def initialize(self):
        self.set_variables()
        self.img_topixel()
        self.bounding()


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

            # if len(pos_set) != 0:
            width = 0
            height = pos_set[0][3]
            for shape in pos_set:
                width += shape[2]
            rect = pygame.Rect(pos_set[0][0],pos_set[0][1],width,height)
            # print(rect)
            self.boundings.append(rect)
            # print(len(pos_set))
                        


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


hut = Graphic('pictures/hut.png',2,[-80,250],[0,255,0], True)
hut.initialize()
hut.pos = [-150, screen_h - hut.h - 6]

character = Graphic('pictures/Owlet_Monster.png',2,[200,50],[0,0,0], True)
character.initialize()




simple_terrain = Terrain(2, [screen_w, screen_h])
tile_sgs = Graphic('pictures/Tile_60.png')
tile_sss = Graphic('pictures/Tile_40.png')
tile_ggg = Graphic('pictures/Tile_02.png')
tile_ssg = Graphic('pictures/Tile_50.png')
tile_no = Graphic('pictures/transparent.png')

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


# bg_y_momentum = 0
L_move = False
R_move = False
U_move = False
D_move = False



test_rect = pygame.Rect(100,100,100,50)

def move_action(w,x,z):
        if L_move:
            character.img_mov('L', w)
        if R_move:
            character.img_mov('R', x)
        if U_move:
            if not character.is_jumping:
                character.is_jumping = True
        if D_move:
            character.img_mov('D', z)

g = 0.5
vo = 0
t = 0

while True:
    screen.fill(b) #elimina el trail de la imagen cargada
    
    simple_terrain.mapping(data,screen)
    hut.graphic_to(screen)
    character.graphic_to(screen)


    # if bg_pos[1] > screen.get_size()[1] - bg.get_height():
    #     bg_y_momentum = -bg_y_momentum
    # else:
    #     bg_y_momentum += 0.2
    # bg_pos[1] += bg_y_momentum


    # bg_rect.y = bg_pos[1]

    if simple_terrain.collide_test(character):
        pygame.draw.rect(screen,r,test_rect)
        character.collision = True
        move_action(4,4,0)
    else:
        pygame.draw.rect(screen,b,test_rect)
        move_action(4,4,4)
        character.collision = False

    if not character.collision and not character.is_jumping:
        # yo = character.pos[1]
        # y = yo + vo*t + 0.5*g*(t**2)
        # t += .5
        # vo = vo + g*t
        if character.vel != character.velinit:
            character.vel += 0.5
        else:
            character.is_jumping = False
        
        character.pos[1] += (0.5*character.mass*(character.vel**2))*character.y_index
        # self.vel -= 0.5

        # character.pos[1] = y
    elif character.collision and not character.is_jumping:
        character.vel = character.velinit
        # vo = 0
        # t = 0

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
                U_move = True
            if event.key == pygame.K_DOWN:
                D_move = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                R_move = False
            if event.key == pygame.K_LEFT:
                L_move = False
            if event.key == pygame.K_UP:
                U_move = False
            if event.key == pygame.K_DOWN:
                D_move = False

    
    pygame.display.update() #actualizar el display, no se actualiza hasta que no se llama este metodo
    pygame.time.Clock().tick(60) #fps

