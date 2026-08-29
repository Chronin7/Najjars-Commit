import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 24)

# State variables
popup_active = False
popup_pos = (0, 0)
options = ["Inspect", "Use", "Destroy"]

# Define the target object (e.g., a chest, an NPC, or a button)
target_object = pygame.Rect(350, 250, 100, 100)

running = True
while running:
  screen.fill((30, 30, 30))

  # Draw the target object
  pygame.draw.rect(screen, (0, 100, 255), target_object)
  txt_target = font.render("Target", True, (255, 255, 255))
  screen.blit(txt_target, (target_object.x + 20, target_object.y + 40))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
      # Right click logic
      if event.button == 3:
        # CRITICAL CHANGE: Check if mouse is over the target object
        if target_object.collidepoint(event.pos):
          popup_active = True
          popup_pos = event.pos
        else:
          popup_active = False  # Close menu if right-clicking empty space

      # Left click logic
      elif event.button == 1 and popup_active:
        x, y = popup_pos
        menu_rect = pygame.Rect(x, y, 120, len(options) * 30)

        if menu_rect.collidepoint(event.pos):
          # Calculate item index based on vertical offset
          clicked_index = (event.pos[1] - y) // 30
          if 0 <= clicked_index < len(options):
            print(f"Action: {options[clicked_index]} on target!")
          popup_active = False
        else:
          popup_active = False  # Clicked outside menu, dismiss it

  # Draw popup menu on top if active
  if popup_active:
    x, y = popup_pos
    menu_rect = pygame.Rect(x, y, 120, len(options) * 30)
    pygame.draw.rect(screen, (50, 50, 50), menu_rect)
    pygame.draw.rect(screen, (200, 200, 200), menu_rect, 2)

    for i, text in enumerate(options):
      txt_surf = font.render(text, True, (255, 255, 255))
      screen.blit(txt_surf, (x + 10, y + 5 + (i * 30)))

  pygame.display.flip()

pygame.quit()
