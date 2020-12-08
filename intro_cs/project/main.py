import pygame
import sys

#inicia el entorno de pygame
pygame.init() 

#inicializando la pantalla
screen = pygame.display.set_mode([400,400])

#le da nombre a la ventana
pygame.display.set_caption("Bricks") 

r = pygame.Color("red")
w = pygame.Color("white")
b = pygame.Color("blue")
black = pygame.Color("black")

# bg = pygame.Surface(screen.get_size())
bg = pygame.Surface((225,150))
bg = bg.convert()
# bg.fill(blue)

bg_location = [50,50]
bg_y_momentum = 0
L_move = False
R_move = False

data = [
    [ w, w, r, r, r, r, r, w, w ],
    [ w, w, r, w, r, w, r, w, w ],
    [ w, w, r, r, r, r, r, w, w ],
    [ w, r, r, r, w, r, r, r, w ],
    [ r, w, w, r, r, r, w, w, r ],
    [ r, r, w, w, w, w, w, r, r ]
]

for y, row in enumerate(data):
    for x, colour in enumerate(row):
        if colour == r:
            rect = pygame.Rect(x*25,y*25,25,25)
            bg.fill(colour, rect=rect)


# player_img = pygame.image.load('path')


while True:
    #blit pone una superficie sobre otra superficie
    # screen.blit(player_img, (50,50)) 
    screen.fill(black) #elimina el trail de la imagen cargada
    screen.blit(bg, bg_location)

    if bg_location[1] > screen.get_size()[1] - bg.get_height():
        bg_y_momentum = -bg_y_momentum
    else:
        bg_y_momentum += 0.2
    bg_location[1] += bg_y_momentum

    if L_move == True:
        bg_location[0] += 4
    if R_move == True:
        bg_location[0] -= 4

    for event in pygame.event.get(): #loop de eventos
        if event.type == pygame.QUIT: #evento de cierre de ventana
            pygame.quit() #primero para pygame
            sys.exit() #detiene el script
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                R_move = True
            if event.key == pygame.K_LEFT:
                L_move = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                R_move = False
            if event.key == pygame.K_LEFT:
                L_move = False

    
    pygame.display.update() #actualizar el display, no se actualiza hasta que no se llama este metodo
    pygame.time.Clock().tick(60) #fps

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# import tensorflow as tf
# if tf.test.gpu_device_name():
#     print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
# else:
#     print("Please install GPU version of TF")

# import tensorflow as tf
# print(tf.__version__)