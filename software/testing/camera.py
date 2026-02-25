import pygame
import numpy as np
from picamera2 import Picamera2

# Initialize pygame
pygame.init()

# Set up display size
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Camera Feed")

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (WIDTH, HEIGHT)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

clock = pygame.time.Clock()
running = True

while running:
    # Capture image as numpy array
    frame = picam2.capture_array()

    # Convert numpy array to Pygame surface
    surface = pygame.surfarray.make_surface(np.rot90(frame))

    # Display on screen
    screen.blit(surface, (0, 0))
    pygame.display.update()

    # Exit on quit or ESC
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    clock.tick(30)  # limit to ~30 FPS

# Clean up
picam2.stop()
pygame.quit()
