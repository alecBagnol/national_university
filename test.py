import pygame
import sys
import cv2 as cv
from PIL import Image
import numpy as np
import matplotlib.image as mpimg

pygame.init()
screen = pygame.display.set_mode([400,400])


# img = Image.open('pictures/snowman.png')
# b = img.load()
# print(b[0])
# img_a = list(np.asarray(Image.open('pictures/snowkid.png').convert('RGB')))
# img_a = Image.open('pictures/snowkid.png')
# img_a = list(img_a.getdata())
# print("PIL ",img_a[0])

# img_b = mpimg.imread('pictures/snowkid.png')
# print("MATPLOT ",img_b[0])

img = cv.imread('pictures/hut.png')
img_surf = pygame.Surface((256,256))
img_pos = [50, 50]
for y, row in enumerate(img):
    for x, col in enumerate(row):
        color_rgb = list(col)
        if color_rgb != [0, 255, 0]:
            rect = pygame.Rect(x*2,y*2,2,2)
            colour = (color_rgb[2],color_rgb[1],color_rgb[0])
            img_surf.fill(colour, rect=rect)
        img_surf.set_colorkey([0,0,0])

# print(list(img[43]))

# player_img = pygame.image.load('pictures/mario.jpg')
# screen.blit(player_img, (50,50)) 
# player_img = player_img.convert()
# # print(player_img)

while True:
    screen.fill('white')
    screen.blit(img_surf, img_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
    pygame.time.Clock().tick(60)




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