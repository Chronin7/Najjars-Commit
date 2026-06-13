import pygame

# ----------------------------
# MAP FILE (SPARSE SYSTEM)
# ----------------------------
def load_room(editor, room_path):
    editor.file = MapFile(room_path)
    editor.load_tiles()
    editor.palette = list(editor.file.definitions.keys())
def parse_definition(line):
    # split hover data
    if ";" in line:
        data_part, hover = line.split(";", 1)
    else:
        data_part, hover = line, None

    parts = data_part.split(":")
    key = parts[0]
    data = parts[1:]

    return key, data, hover
class MapFile:
    def __init__(self, path):
        self.path = path
        self.sync()
    def sync(self):
        self.definitions = {}
        self.hover = {}   # NEW: hover metadata
        self.tiles = {}

        with open(self.path, "r") as file:
            lines = [l.strip() for l in file if l.strip()]

        mode = None
        y = 0

        for line in lines:

            if line == "[DEFS]":
                mode = "defs"
                continue

            if line == "[MAP]":
                mode = "map"
                continue

            # --------------------
            # DEFINITIONS
            # --------------------
            if mode == "defs":

                key, data, hover = parse_definition(line)

                self.definitions[key] = data

                if hover:
                    self.hover[key] = hover

            # --------------------
            # MAP
            # --------------------
            elif mode == "map":

                row = line.split(",")

                for x, cell in enumerate(row):
                    if cell != "n":
                        self.tiles[(x, y)] = cell

                y += 1
    def save(self):
        # Safely capture boundaries even if the user paints into negative coordinates
        if self.tiles:
            min_x = min(x for x, y in self.tiles.keys())
            max_x = max(x for x, y in self.tiles.keys())
            min_y = min(y for x, y in self.tiles.keys())
            max_y = max(y for x, y in self.tiles.keys())
        else:
            min_x = max_x = min_y = max_y = 0

        with open(self.path, "w") as f:
            # 1. Write definitions section
            f.write("[DEFS]\n")
            for k, v in self.definitions.items():
                hover_suffix = f";{self.hover[k]}" if k in self.hover else ""
                f.write(f"{k}:{':'.join(v)}{hover_suffix}\n")

            f.write("\n[MAP]\n")

            # 2. Rebuild dense grid layout from sparse coordinates
            for y in range(min_y, max_y + 1):
                row = []
                for x in range(min_x, max_x + 1):
                    row.append(self.tiles.get((x, y), "n"))
                f.write(",".join(row) + "\n")


# ----------------------------
# TILE
# ----------------------------

class Tile:
    def __init__(self, path):
        if path == "null.png":
            # Create a 32x32 completely transparent surface
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))  # 0 alpha means 100% clear
        else:
            try:
                self.image = pygame.image.load(path).convert_alpha()
            except pygame.error:
                self.image = pygame.Surface((32, 32))
                self.image.fill((80, 200, 80))


# ----------------------------
# EDITOR
# ----------------------------

class MapEditor:
    def __init__(self, path):
        self.file = MapFile(path)

        self.tile_size = 32
        self.camera_x = 0
        self.camera_y = 0

        self.tiles = {}
        self.load_tiles()

        self.palette = list(self.file.definitions.keys())
        self.selected_index = 0
        self.context_tile = None
        self.context_pos = (0, 0)
        self.menu_open = False
        self.center_camera()

    # ----------------------------
    # LOAD SPRITES
    # ----------------------------
    def load_tiles(self):
        self.tiles = {}

        for key, value in self.file.definitions.items():

            asset = value[0]

            # NORMAL TILE (PNG)
            if asset.endswith(".png"):
                self.tiles[key] = Tile(asset)

            # ENTITY / DOOR / SPECIAL OBJECT
            else:
                self.tiles[key] = {
                    "type": "special",
                    "data": value
                }
            

    # ----------------------------
    # CAMERA CENTER
    # ----------------------------

    def center_camera(self):
        if not self.file.tiles:
            return

        max_x = max(x for x, y in self.file.tiles.keys())
        max_y = max(y for x, y in self.file.tiles.keys())

        self.camera_x = (max_x * self.tile_size) // 2 - W // 2
        self.camera_y = (max_y * self.tile_size) // 2 - H // 2

    # ----------------------------
    # GRID CONVERSION
    # ----------------------------

    def screen_to_grid(self, x, y):
        gx = (x + self.camera_x) // self.tile_size
        gy = (y + self.camera_y) // self.tile_size
        return int(gx), int(gy)

    # ----------------------------
    # PAINT (AUTO EXPAND WORLD)
    # ----------------------------

    def paint(self, x, y):
        key = self.palette[self.selected_index]
        self.file.tiles[(x, y)] = key

    # ----------------------------
    # PALETTE SCROLL
    # ----------------------------

    def scroll(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.palette)

    # ----------------------------
    # SAVE
    # ----------------------------

    def save(self):
        self.file.save()


# ----------------------------
# MAIN
# ----------------------------

def main():
    tic=0
    pygame.init()

    global W, H
    W, H = 800, 600
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    editor = MapEditor("test.map")

    running = True
    down=False
    menu=False
    while running:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # paint
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button!=3:
                    down=True
            if down:
                mx, my = pygame.mouse.get_pos()
                gx, gy = editor.screen_to_grid(mx, my)
                editor.paint(gx, gy)
            if event.type==pygame.MOUSEBUTTONUP:
                down=False
                if event.button == 3:
                    menu=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    menu=True
            if menu:
                mx, my = pygame.mouse.get_pos()
                gx, gy = editor.screen_to_grid(mx, my)

                editor.context_tile = editor.file.tiles.get((gx, gy))
                editor.context_pos = (gx, gy)
                editor.menu_open = True
                    

        # camera
        keys = pygame.key.get_pressed()
        speed = 5
        if keys[pygame.K_a]:
            editor.camera_x -= speed
        if keys[pygame.K_d]:
            editor.camera_x += speed
        if keys[pygame.K_w]:
            editor.camera_y -= speed
        if keys[pygame.K_s]:
            editor.camera_y += speed
        if keys[pygame.K_MINUS] and tic<0:
            editor.scroll(-1)
            tic=5
        if keys[pygame.K_EQUALS] and tic<0:
            editor.scroll(1)
            tic=5
        if keys[pygame.K_i]:
            editor.save()
        tic-=1
        # draw
        screen.fill((20, 20, 20))
        for (x, y), cell in editor.file.tiles.items():

            sx = x * editor.tile_size - editor.camera_x
            sy = y * editor.tile_size - editor.camera_y

            tile_obj = editor.tiles.get(cell)

            if isinstance(tile_obj, Tile):
                img = pygame.transform.scale(
                    tile_obj.image,
                    (editor.tile_size, editor.tile_size)
                )
                screen.blit(img, (sx, sy))

            else:
                # SPECIAL OBJECT RENDER (door/entity placeholder)
                pygame.draw.rect(
                    screen,
                    (200, 80, 80),
                    (sx, sy, editor.tile_size, editor.tile_size)
                )

        # UI
        font = pygame.font.SysFont(None, 24)
        selected = editor.palette[editor.selected_index]

        text = font.render(
            f"Selected: {selected}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (10, 10))
        mx, my = pygame.mouse.get_pos()
        gx = (mx + editor.camera_x) // editor.tile_size
        gy = (my + editor.camera_y) // editor.tile_size
        tile_id = editor.file.tiles.get((gx, gy))
        hover_text = None

        if tile_id:
            hover_text = editor.file.hover.get(tile_id)
        if hover_text:
            font = pygame.font.SysFont(None, 24)

            text_surface = font.render(
                hover_text,
                True,
                (255, 255, 255)
            )

            # background box
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (mx + 10, my + 10, text_surface.get_width() + 6, text_surface.get_height() + 6)
            )
            if editor.menu_open:

                mx, my = pygame.mouse.get_pos()

                menu_w, menu_h = 160, 80

                pygame.draw.rect(screen, (30, 30, 30), (mx, my, menu_w, menu_h))
                pygame.draw.rect(screen, (255, 255, 255), (mx, my, menu_w, menu_h), 2)

                font = pygame.font.SysFont(None, 22)

                t1 = font.render("1. Edit Metadata", True, (255, 255, 255))
                t2 = font.render("2. Go To Room", True, (255, 255, 255))

                screen.blit(t1, (mx + 10, my + 10))
                screen.blit(t2, (mx + 10, my + 35))
                if editor.menu_open:

                    mx, my = pygame.mouse.get_pos()

                    # click inside menu
                    if keys[pygame.K_1]:
                        print("OPEN METADATA EDITOR")
                    elif keys[pygame.K_2]:
                        tile = editor.context_tile

                        if tile:
                            data = editor.file.definitions.get(tile)

                            if data and len(data) >= 3:
                                room = data[1]
                                x = int(data[2])
                                y = int(data[3])

                                load_room(editor, room)



                    editor.menu_open = False
            screen.blit(text_surface, (mx + 13, my + 13))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()