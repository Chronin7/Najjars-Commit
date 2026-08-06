import pygame,time

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
class MapEditor:

    def __init__(self, path):

        self.file = MapFile(path)

        self.tile_size = 32

        self.camera_x = 0
        self.camera_y = 0

        self.menu_open = False
        self.menu_screen_pos = (0, 0)
        self.context_pos = (0, 0)

        self.palette = list(self.file.definitions.keys())
        self.selected_index = 0

        self.tile_images = {}

        self.load_tiles()

    # -------------------------
    # LOAD TILE IMAGES
    # -------------------------

    def load_tiles(self):

        self.tile_images.clear()

        for key, data in self.file.definitions.items():

            asset = data[0]

            if asset.endswith(".png"):

                try:
                    image = pygame.image.load(asset).convert_alpha()

                except:

                    image = pygame.Surface((32, 32))
                    image.fill((255, 0, 255))

                self.tile_images[key] = image

    # -------------------------
    # GRID CONVERSION
    # -------------------------

    def screen_to_grid(self, sx, sy):

        gx = (sx + self.camera_x) // self.tile_size
        gy = (sy + self.camera_y) // self.tile_size

        return int(gx), int(gy)

    # -------------------------
    # PAINT
    # -------------------------

    def paint(self, x, y):
        print(x,y)
        tile = self.palette[self.selected_index]
        if (x, y) in self.file.metadata.keys():

            self.file.metadata.pop((x,y))
            print("popd")
        if tile == "n":

            self.file.tiles.pop((x, y), None)

        else:

            self.file.tiles[(x, y)] = tile

    # -------------------------
    # TILE SELECTION
    # -------------------------

    def scroll(self, amount):

        self.selected_index += amount

        self.selected_index %= len(self.palette)

    # -------------------------
    # SAVE
    # -------------------------

    def save(self):

        self.file.save()

    # -------------------------
    # DRAW GRID
    # -------------------------

    def draw_grid(self, screen):

        left = self.camera_x // self.tile_size
        top = self.camera_y // self.tile_size

        right = left + screen.get_width() // self.tile_size + 2
        bottom = top + screen.get_height() // self.tile_size + 2

        for x in range(left, right):

            sx = x * self.tile_size - self.camera_x

            pygame.draw.line(
                screen,
                (40, 40, 40),
                (sx, 0),
                (sx, screen.get_height())
            )

        for y in range(top, bottom):

            sy = y * self.tile_size - self.camera_y

            pygame.draw.line(
                screen,
                (40, 40, 40),
                (0, sy),
                (screen.get_width(), sy)
            )

    # -------------------------
    # DRAW TILES
    # -------------------------

    def draw_tiles(self, screen):

        for (x, y), tile in self.file.tiles.items():

            sx = x * self.tile_size - self.camera_x
            sy = y * self.tile_size - self.camera_y

            if tile in self.tile_images:

                img = pygame.transform.scale(
                    self.tile_images[tile],
                    (self.tile_size, self.tile_size)
                )

                screen.blit(img, (sx, sy))

    # -------------------------
    # DRAW METADATA OBJECTS
    # -------------------------

    def draw_metadata(self, screen):

        for (x, y), meta in self.file.metadata.items():

            if len(meta["data"]) == 0:
                continue

            sprite = meta["data"][0]

            if not sprite.endswith(".png"):
                continue

            try:

                img = pygame.image.load(sprite).convert_alpha()

                img = pygame.transform.scale(
                    img,
                    (self.tile_size, self.tile_size)
                )

                sx = x * self.tile_size - self.camera_x
                sy = y * self.tile_size - self.camera_y

                screen.blit(img, (sx, sy))

            except:
                pass

    # -------------------------
    # DRAW SELECTED TILE UI
    # -------------------------

    def draw_ui(self, screen):

        font = pygame.font.SysFont(None, 24)

        selected = self.palette[self.selected_index]

        text = font.render(
            f"Selected: {selected}",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (10, 10))

    # -------------------------
    # MAIN DRAW
    # -------------------------

    def draw(self, screen):

        self.draw_grid(screen)

        self.draw_tiles(screen)

        self.draw_metadata(screen)

        self.draw_ui(screen)# ----------------------------
# TILE
# ----------------------------

class Tile:
    def __init__(self, path,metadata=None):
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
        if metadata:
            self.metadata=metadata
    def __str__(self):
        pass

# ----------------------------
# EDITOR
# ----------------------------

class MapFile:
    def __init__(self, path):
        self.path = path
        self.sync()

    def sync(self):

        self.definitions = {}
        self.tiles = {}
        self.metadata = {}

        with open(self.path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        mode = None
        y = 0

        for line in lines:

            if line == "[DEFS]":
                mode = "defs"
                continue

            if line == "[MAP]":
                mode = "map"
                continue

            if line == "[metadata]":
                mode = "metadata"
                continue

            # -----------------
            # DEFINITIONS
            # -----------------

            if mode == "defs":

                key, *data = line.split(":")
                self.definitions[key] = data

            # -----------------
            # MAP
            # -----------------

            elif mode == "map":

                row = line.split(",")

                for x, cell in enumerate(row):

                    if cell != "n":
                        self.tiles[(x, y)] = cell

                y += 1

            # -----------------
            # METADATA
            # -----------------

            elif mode == "metadata":

                pos, rest = line.split(":", 1)

                x, y = map(int, pos.split(","))

                if ";" in rest:
                    data_part, hover = rest.split(";", 1)
                else:
                    data_part = rest
                    hover = ""

                data = data_part.split(":")

                self.metadata[(x, y)] = {
                    "data": data,
                    "hover": hover
                }

def get_context_menu(editor):
    menu = ["METADATA"]

    meta = editor.file.metadata.get(editor.context_pos)

    if meta and "door" in meta.get("hover", ""):
        menu = ["GTR", "METADATA"]

    return menu

# ----------------------------
# MAIN
# ----------------------------

def main():
    pygame.init()
    global W, H
    W, H = 1280, 720

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Map Editor")

    clock = pygame.time.Clock()

    editor = MapEditor("test.map")

    running = True
    painting = False
    tic=0
    while running:

        dt = clock.tick(60)

        # --------------------
        # EVENTS
        # --------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("click")
                # LEFT CLICK
                if event.button == 1:
                    if editor.menu_open:
                        editor.menu_open=False
                        print("menu false")
                    else:
                        painting = True
                        print("painting true")
                # RIGHT CLICK
                elif event.button == 3:

                    mx, my = pygame.mouse.get_pos()

                    gx, gy = editor.screen_to_grid(mx, my)

                    editor.context_pos = (gx, gy)
                    editor.menu_open = True
                    editor.menu_screen_pos = (mx, my)

            if event.type == pygame.MOUSEBUTTONUP:
                print("unclick")
                if event.button == 1:
                    painting = False

            if event.type == pygame.MOUSEWHEEL:

                if event.y > 0:
                    editor.scroll(-1)

                elif event.y < 0:
                    editor.scroll(1)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_i:
                editor.save()
            if event.key==pygame.K_k:
                print("ho")
            if event.key == pygame.K_ESCAPE:
                editor.menu_open = False

            if editor.menu_open:
                menu = get_context_menu(editor)

                if event.key == pygame.K_1:
                    print("hi")
                    if "METADATA" in menu:
                        meta = editor.file.metadata.get(editor.context_pos)
                        print("Edit metadata:", editor.context_pos, meta)

                        # Put your metadata editor code here later.
                        # For now this proves the key works.

                if event.key == pygame.K_2:
                    if "GTR" in menu:
                        meta = editor.file.metadata.get(editor.context_pos)

                        if meta and len(meta["data"]) > 1:
                            room_path = meta["data"][1]
                            print("Going to room:", room_path)

                            load_room(editor, room_path)
                            editor.menu_open = False

        # --------------------
        # PAINTING
        # --------------------

        if painting:

            mx, my = pygame.mouse.get_pos()

            gx, gy = editor.screen_to_grid(mx, my)

            editor.paint(gx, gy)

        # --------------------
        # CAMERA
        # --------------------

        keys = pygame.key.get_pressed()

        speed = 10

        if keys[pygame.K_a]:
            editor.camera_x -= speed

        if keys[pygame.K_d]:
            editor.camera_x += speed

        if keys[pygame.K_w]:
            editor.camera_y -= speed

        if keys[pygame.K_s]:
            editor.camera_y += speed
        if keys[pygame.K_PLUS] and tic<1:
            editor.scroll(1)
            tic=10
        if keys[pygame.K_EQUALS] and tic<1:
            editor.scroll(-1)
            tic=10
        tic-=1
        
        if editor.menu_open:
            meta = editor.file.metadata.get(editor.context_pos)
            menu = ["METADATA"]

            if meta and "door" in meta.get("hover", ""):
                menu = ["GTR", "METADATA"]



        # --------------------
        # DRAW
        # --------------------

        screen.fill((20, 20, 20))

        editor.draw(screen)

        # --------------------
        # HOVER TOOLTIP
        # --------------------

        mx, my = pygame.mouse.get_pos()

        gx, gy = editor.screen_to_grid(mx, my)

        meta = editor.file.metadata.get((gx, gy))

        if meta:

            hover_text = meta["hover"]

            if hover_text and not painting:

                font = pygame.font.SysFont(None, 24)

                text_surface = font.render(
                    hover_text,
                    True,
                    (255, 255, 255)
                )

                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (
                        mx + 10,
                        my + 10,
                        text_surface.get_width() + 10,
                        text_surface.get_height() + 10
                    )
                )

                screen.blit(
                    text_surface,
                    (mx + 15, my + 15)
                )

        # --------------------
        # CONTEXT MENU
        # --------------------

        if editor.menu_open:
            menu = get_context_menu(editor)

            menu_x, menu_y = editor.menu_screen_pos
            height = 80 if "GTR" in menu else 40

            pygame.draw.rect(
                screen,
                (40, 40, 40),
                (menu_x, menu_y, 220, height)
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (menu_x, menu_y, 220, height),
                2
            )

            font = pygame.font.SysFont(None, 24)

            if "METADATA" in menu:
                screen.blit(
                    font.render("1 Edit Metadata", True, (255, 255, 255)),
                    (menu_x + 10, menu_y + 10)
                )

            if "GTR" in menu:
                screen.blit(
                    font.render("2 Go To Room", True, (255, 255, 255)),
                    (menu_x + 10, menu_y + 40)
                )

        else:
            menu = []
        # --------------------
        # SELECTED TILE UI
        # --------------------

        font = pygame.font.SysFont(None, 24)

        selected = editor.palette[editor.selected_index]

        screen.blit(
            font.render(
                f"Selected: {selected}",
                True,
                (255,255,255)
            ),
            (10,10)
        )

        pygame.display.flip()

    pygame.quit()
main()