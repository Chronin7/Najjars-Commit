from ursina import *

app = Ursina()

# Create a 3D cube with a box collider
cube = Entity(model='cube', color=color.azure, scale=2, collider='box')

# Define what happens when the cube is clicked
def spin():
    cube.animate('rotation_y', cube.rotation_y + 360, duration=2, curve=curve.in_out_expo)

cube.on_click = spin

# Add camera controls to orbit/move with the mouse
EditorCamera()

app.run()