import pygame
import util_functions
import tkinter as tk
from tkinter import simpledialog

# Hide the main root window that tkinter creates by default
root = tk.Tk()
root.withdraw()

live_window = tk.Toplevel(root)
live_window.title("Live Tile Metadata")
live_window.geometry("300x100")
# Keep it on top of the Pygame screen
live_window.attributes("-topmost", True)
size=20
# A label inside the window to display the text
metadata_label = tk.Label(live_window, text="Hover or select a tile...", font=("Arial", 12), wraplength=280)
metadata_label.pack(pady=size)

RED= (255,0,0)
BLACK=(0,0,0)
screen_width = 1000
screen_height = 1000

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tile Editor")

def render(popup_active,active_tile,text_surface,x,y,screen):
    global size
    screen.fill(BLACK)
    for xx in tiles:
        for yy in xx:
            if type(yy)==tile:
                yy.render()
    screen.blit(text_surface, (50,50))
    if popup_active and active_tile:
        x, y = popup_pos
        num_options = len(active_tile.options)
        menu_rect = pygame.Rect(x, y, 140, num_options * 25)
        pygame.draw.rect(screen, (40, 40, 40), menu_rect) # Background
        pygame.draw.rect(screen, (200, 200, 200), menu_rect, 1) # Border
        for i, (key, text) in enumerate(active_tile.options.items()):
            txt_surf = font.render(text, True, (255, 255, 255))
            screen.blit(txt_surf, (x + 8, y + 4 + (i * 25)))
    pygame.display.flip()

font = pygame.font.Font(size=size)
running=True
clock = pygame.time.Clock()
tile_ops=[]
make_tiles = lambda n=1000: [[""] * n for _ in range(n)]
tiles = make_tiles()

class tile:
    def __init__(self,png_path,metadata,location,options={0:"change metadata"}):
        global tiles,size
        original_image = pygame.image.load(png_path).convert_alpha()
        target_size = (size,size)
        self.location=location
        self.metadata=metadata
        self.unmodlocation=location
        self.options=options
        self.scaled_image = pygame.transform.scale(original_image, target_size)
        if location!=None:
            tiles[int(location[0]/size)][int(location[1]/size)]=self
            
    def render(self):
        screen.blit(self.scaled_image, (self.location[0],self.location[1]))
    def change(self,new_png=None,new_metadata=None,new_options=None,new_pos=None):
        if new_pos!=None:
            self.location=new_pos
        if new_png!=None:
            self.png_path=new_png
            original_image = pygame.image.load(self.png_path).convert_alpha()
            target_size = (size,size)
            self.scaled_image = pygame.transform.scale(original_image, target_size)
        if new_metadata!=None:
            self.metadata=new_metadata
        if new_options!=None:
            self.options=new_options
    def scail(self):
        self.location=[self.unmodlocation[0]*size,self.unmodlocation[1]*size]
wall=["wall.png",""]
tile_ops.append(wall)
enemie=["enemie.png","bob"]
tile_ops.append(enemie)
door=["door.png",{"destination":"","location":(0,0)}]
tile_ops.append(door)
num=0
c_tile=tile_ops[num]

popup_active = False
popup_pos = (0, 0)
active_tile = None
x, y = popup_pos
tic=0

while running:
    pos = pygame.mouse.get_pos()
    
    # Live update window text when hovering over any valid grid tile dynamically
    hover_x = int(pos[0] / size)
    hover_y = int(pos[1] / size)
    if 0 <= hover_x < 50 and 0 <= hover_y < 50 and type(tiles[hover_x][hover_y]) == tile:
        metadata_label.config(text=f"Hovering Metadata:\n{tiles[hover_x][hover_y].metadata}")
    elif not popup_active:
        metadata_label.config(text="Hover or select a tile...")

    # 1. Handle Window Closing & Scrolling (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3: # Middle click to OPEN the menu
                tic=10000
                grid_x = int(event.pos[0] / size)
                grid_y = int(event.pos[1] / size)
                if 0 <= grid_x < 50 and 0 <= grid_y < 50 and type(tiles[grid_x][grid_y]) == tile:
                    popup_active = True
                    popup_pos = event.pos
                    active_tile = tiles[grid_x][grid_y]
                    metadata_label.config(text=f"Selected Metadata:\n{active_tile.metadata}")
                else:
                    popup_active = False
            elif event.button == 1: # Left click to SELECT menu options
                if popup_active and active_tile:
                    x, y = popup_pos
                    num_options = len(active_tile.options)
                    menu_rect = pygame.Rect(x, y, 140, num_options * 25)
                    if menu_rect.collidepoint(event.pos):
                        clicked_index = (event.pos[1] - y) // 25
                        if 0 <= clicked_index < num_options:
                            option_text = list(active_tile.options.values())[clicked_index]
                            
                            if option_text == "change metadata":
                                # Open text dialogue window to write new metadata
                                new_meta = simpledialog.askstring("Edit Metadata", "Enter new tile metadata:", initialvalue=active_tile.metadata)
                                if new_meta is not None:
                                    active_tile.metadata = new_meta
                                    metadata_label.config(text=f"Updated Metadata:\n{active_tile.metadata}")
                            if option_text=="go to room":
                                print("wip")
                                    
                        popup_active = False
                    else:
                        popup_active = False # Clicked away from menu
                    tic=0
            elif event.button == 4: # Scroll Up
                num = (num + 1) % len(tile_ops)
                c_tile = tile_ops[num]
            elif event.button == 5: # Scroll Down
                num = (num - 1) % len(tile_ops)
                c_tile = tile_ops[num]
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_s: #front side button
                pass
            elif event.key==pygame.K_w: #back side button
                pass
            elif event.key==pygame.K_d: #bottom button
                pass
            elif event.key==pygame.K_e: #side scroll up
                size-=1
                for xx in tiles:
                    for yy in xx:
                        if type(yy)==tile:
                            yy.scail()
                pass #zoom in
            elif event.key==pygame.K_q: #side scroll down
                size+=1
                for xx in tiles:
                    for yy in xx:
                        if type(yy)==tile:
                            yy.scail()
                pass #zoom out
            elif event.key==pygame.K_a: #top middle button
                pass

    # 2. Continuous Paint / Erase Logic (Every Frame)
    grid_x = int(pos[0] / size)
    grid_y = int(pos[1] / size)
    mouse_buttons = pygame.mouse.get_pressed()
    
    if not popup_active and tic<0:
        if mouse_buttons[0]: # Left mouse button held down
            snap_x = grid_x * size
            snap_y = grid_y * size
            if tiles[grid_x][grid_y]=="":
                if c_tile[0]=="door.png":
                    tile(c_tile[0], c_tile[1], (snap_x, snap_y),options={0:"change metadata",1:"go to room"})
                else:
                    tile(c_tile[0], c_tile[1], (snap_x, snap_y))
        elif mouse_buttons[1]: # Right mouse button held down
            tiles[grid_x][grid_y] = ""
    tic-=1

    # 3. Render and Tick
    text_surface = font.render(f"{c_tile[0]}:{c_tile[1]}", True, (255,255,255))
    render(popup_active,active_tile,text_surface,x,y,screen)
    root.update()
    clock.tick(60)
