import pygame, os, time

# Global list to store joystick objects
joysticks = []

def init():
    global joysticks
    pygame.init()
    pygame.joystick.init()
    time.sleep(1)  # Allow time for OS to register joystick
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for js in joysticks:
        js.init()
    print(f"Detected {len(joysticks)} joystick(s).")
    for i, js in enumerate(joysticks):
        print(f"Joystick {i}: {js.get_name()}")

def get_status():
    pygame.event.pump()  # Update joystick state
    axes_list = []
    buttons_list = []
    for js in joysticks:
        axes = [round(js.get_axis(a), 3) for a in range(js.get_numaxes())]
        buttons = [js.get_button(b) for b in range(js.get_numbuttons())]
        axes_list.append(axes)
        buttons_list.append(buttons)
    return axes_list, buttons_list

def end():
    for js in joysticks:
        js.quit()
    pygame.joystick.quit()
    pygame.quit()
    print("Joystick and Pygame shutdown complete.")
if __name__=="__main__":
	init()

	try:
		while True:
			axes, buttons = get_status()
			os.system('cls' if os.name == 'nt' else 'clear')
			for i in range(len(axes)):
				print(f"Joystick {i} axes: {axes[i]}")
				print(f"Joystick {i} buttons: {buttons[i]}")
				print(buttons)
			time.sleep(0.1)
	except KeyboardInterrupt:
		end()