import pygame
import util_functions
RED= (255,0,0)
BLACK=(0,0,0)
screen_width = 1000
screen_height = 1000
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tile Editor")
def render(board,paths):
    screen.fill(BLACK)
    for x in tiles:
        for y in x:

            if type(y)==tile:
                y.render()
            

    pygame.display.flip()

running=True
clock = pygame.time.Clock()
tile_ops=[]
make_tiles = lambda n=50: [[""] * n for _ in range(n)]

tiles = make_tiles()
class tile:
    def __init__(self,png_path,metadata,location,options={0:"get metadata"}):
        global tiles
        original_image = pygame.image.load(png_path).convert_alpha()
        target_size = (20,20)
        self.location=location
        self.metadata=metadata
        self.options=options
        self.scaled_image = pygame.transform.scale(original_image, target_size)
        if location!=None:
            tiles[int(location[0]/20)][int(location[1]/20)]=self
        

    def render(self):
            screen.blit(self.scaled_image, (self.location[0],self.location[1]))
    def change(self,new_png=None,new_metadata=None,new_options=None,new_pos=None):
        if new_pos!=None:
            self.location=new_pos
        if new_png!=None:
            self.png_path=new_png
            original_image = pygame.image.load(self.png_path).convert_alpha()
            target_size = (20,20)
            self.scaled_image = pygame.transform.scale(original_image, target_size)
        if new_metadata!=None:
            self.metadata=new_metadata
        if new_options!=None:
            self.options=new_options
        
        
wall=["wall.png",""]
tile_ops.append(wall)
enemie=["enemie.png",""]
tile_ops.append(enemie)
num=0
c_tile=tile_ops[0]
while running:
    pos = pygame.mouse.get_pos()
    
    # 1. Handle Window Closing & Scrolling (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll Up
                num = (num + 1) % len(tile_ops)
                c_tile = tile_ops[num]
            elif event.button == 5:  # Scroll Down
                num = (num - 1) % len(tile_ops)
                c_tile = tile_ops[num]

    # 2. Continuous Paint / Erase Logic (Every Frame)
    grid_x = int(pos[0] / 20)
    grid_y = int(pos[1] / 20)
    
    # Get the state of all mouse buttons: (Left, Middle, Right)
    mouse_buttons = pygame.mouse.get_pressed()
    
    if mouse_buttons[0]:  # Left mouse button is being HELD DOWN
        # Only create a new tile if the space isn't already occupied by this type
        # This keeps your code fast by not creating thousands of duplicate Tile objects
        snap_x = grid_x * 20
        snap_y = grid_y * 20
        
        if tiles[grid_x][grid_y] == "":
            tile(c_tile[0], c_tile[1], (snap_x, snap_y))
            
    elif mouse_buttons[2]:  # Right mouse button is being HELD DOWN
        tiles[grid_x][grid_y] = ""

    # 3. Render and Tick
    render(tiles,0)
    clock.tick(60)
