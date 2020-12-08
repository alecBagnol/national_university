import pygame
import sys

pygame.init() #inicia el entorno de pygame
screen = pygame.display.set_mode([400,400])#inicializando la pantalla

pygame.display.set_caption("Bricks") #le da nombre a la ventan

r = pygame.Color("red")
w = pygame.Color("white")
black = pygame.Color("black")

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
        rect = pygame.Rect(x*25,y*25,25,25)
        screen.fill(colour, rect=rect)


# player_img = pygame.image.load('path')
L_move = False
R_move = False

while True:
    #blit pone una superficie sobre otra superficie
    # screen.blit(player_img, (50,50)) 

    for event in pygame.event.get(): #loop de eventos
        if event.type == pygame.QUIT: #evento de cierre de ventana
            pygame.quit() #primero para pygame
            sys.exit() #detiene el script
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                R_move = True
                screen.fill(black)
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