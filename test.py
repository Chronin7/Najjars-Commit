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
            if asset.endswith(":metadata"):
                
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