# Game development approach

<img src="https://raw.githubusercontent.com/alecBagnol/national_university/master/intro_cs/project/pictures/screenshot.png">

### This is an aproximation to dealing with physics and other things related to creating a game, particularly a platformer; all in order to build a better understanding and for future reference.

First, I had to deal with how to place images and render them correctly on the screen, and I went with the pixel by pixel approach, loading an image and doing pixel operations like scaling an then taking them to the pygame canvas.


I get the image matrix by loading it with openCV and though width and height references could be inferred with the length of the array obtained, I went by getting this metadata by calling openCV methods.
```python
def img_std(self):
        self.img = cv.imread(self.pic_path)
        self.shape = self.img.shape
        self.w = self.shape[1] * self.ratio
        self.h = self.shape[0] * self.ratio
        self.surf = pygame.Surface((self.w, self.h))
        self.img_topixel(self.img, self.surf)
```
Once I had the image matrix data, I just went by looping the array and drawing rectangles, taking into account an scale index called in this case *ratio* and then setting it into a pygame surface.

Initially I thought that setting a color key for making exceptions at the momment of drawing a pixel in a pygames surface could make a difference, but the thing is that it seems Pygame set a surface with a solid alpha index of 255, and so i had to tell the interface that I was loading a transparent graphic by setting the alpha to 0, or setting a color_key.
```python
for y, row in enumerate(cvimage):
        for x, col in enumerate(row):
            color_rgb = list(col)
            if color_rgb != self.key:
                rect = pygame.Rect(x*self.ratio,y*self.ratio,self.ratio,self.ratio)
                colour = (color_rgb[2],color_rgb[1],color_rgb[0])
                surface.fill(colour, rect=rect)
    surface.set_colorkey([0,0,0])
```

I had the idea of creating a class to load the images and then with the graphic loaded within an object I could manipulate it with more flexibility, but initially I didn't take into account the frame rates and how much the game time would differ from the real time for managing animations among others. So in order not just to improve my understanding of classes but to better structure the game data, I'll have to re-structure in general the graphics and terrain classes.

### *"Think in framerates, not in seconds"*

I also went by the idea of creating my own collision detection method for the graphic object class. The idea behind was that every graphic has to be within a rectangle,  and that the possition coordinates, and width and heigh of the picture could form and help to differentiate the object bounds.

So if two bounding areas *a* and *b* came in contact with each other, they will tell by referencing the bounding possition as accordingly with the next logic:
``` python
if a_x < b_x + b_width and a_x + a_width > b_x and a_y < b_y + b_height and a_y + a_height > b_y: 
    #Collision logic
```

I then went by exploring how to render the terrain...I though that placing an image and setting imaginary bounding areas will do the trick but how wrong I was...
I then came to the conclusion *(and after referencing some work on how game devs rendered tiles)* that it could be best to load the tiles by using a "Tile Map".
```python
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

while True:
    clock.tick(60) #fps
    screen.fill(b) #get rid of the rail image residue
    simple_terrain.mapping(data,screen)
```
Then, I created and object where I loaded the tiles .The idea was to append each tile to a tile array that has setted the first element of the array as null, making the 0 call as no tile, and from 1 forward I would define a different texture. Each element was loaded as a graphic object, and as so, each will have a bounding area.

One think that I didn't have idea of how it will develop and that I just naively obviated initially was the "how to jump" or "how to throw rocks"... it seemed natural but Oh Boy!... game physics are a hole niche and in order to perceive a nice looking jump *(or at least an aproximation)* I had to rock out my physics 101 lectures.. 

```python
def load_jump_animation(self, path):
    self.jump_img = cv.imread(path)
    self.jump_shape = self.jump_img.shape
    self.jump_w = self.jump_shape[1] * self.ratio
    self.jump_h = self.jump_shape[0] * self.ratio
    self.jump_surf = pygame.Surface((self.jump_w, self.jump_h))
    self.img_topixel(self.jump_img, self.jump_surf)

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

character.load_jump_animation('pictures/Owl_jump.png')
jump_around = False

while True:
    clock.tick(60) #fps

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
```
After iterating some ideas, I end up using a approach to the Kinetic Energy equation: 
># <img src="https://render.githubusercontent.com/render/math?math=KE = \frac{1}{2} mv^{2}">
```python
self.pos[1] -= (0.5*self.mass*(self.vel**2))*self.y_index
```
This with an index that once velocity reached 0 it will stop the jump execution and let the general *"gravity"* take over the character, all this with the idea of creating a different motion perception, similar to what Mario from Super Mario Bros does.

All ok until you have to take into account the animation... and that's something I'm still figuring out.. how to match the jumping stages with the framerate of a determined animation given to an action. At the moment I'm taking into account the general framerate speed of 60 frames per seconds *(Given by the clock method in pygame)* and operating it with an integer division in order to get a change of sprite in a given number of frames.
```python
frame_counter = jump_counter//5
...
if jump_counter % 5 == 0:
    ...
```
That conditional will keep changing up the frames until the final frame index is reached, and once that final frame is reached, it will restart the animation.