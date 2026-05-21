from ursina import *

app = Ursina(title="Work Project", borderless=False, fullscreen=False, size=(400,300))
Entity(model='quad', color=color.green)

app.run()