import pygame
import RPi.GPIO as GPIO
import time
import sys

# GPIO setup
IN1, IN2 = 17, 18
IN3, IN4 = 22, 23
ENA, ENB = 27, 24

GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)
pwm_ENA = GPIO.PWM(ENA, 1000)
pwm_ENB = GPIO.PWM(ENB, 1000)
pwm_ENA.start(0)
pwm_ENB.start(0)

def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(100)
    pwm_ENB.ChangeDutyCycle(100)

def move_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(100)
    pwm_ENB.ChangeDutyCycle(100)

def turn_left():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(100)
    pwm_ENB.ChangeDutyCycle(100)

def turn_right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(100)
    pwm_ENB.ChangeDutyCycle(100)

def stop_motors():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(0)
    pwm_ENB.ChangeDutyCycle(0)

# Pygame UI setup
pygame.init()
screen = pygame.display.set_mode((1024, 600))
pygame.display.set_caption("Robot Touch Controller")

WHITE = (255, 255, 255)
BG = (240, 240, 240)
BLUE = (50, 120, 255)
BLUE_HIGHLIGHT = (100, 180, 255)

# Define control zones
forward_rect = pygame.Rect(462, 80, 100, 100)
backward_rect = pygame.Rect(462, 420, 100, 100)
left_rect = pygame.Rect(262, 250, 100, 100)
right_rect = pygame.Rect(662, 250, 100, 100)

highlighted_command = None

def draw_arrow(surface, points, is_active):
    color = BLUE_HIGHLIGHT if is_active else BLUE
    pygame.draw.polygon(surface, color, points)

current_command = None
running = True

try:
    while running:
        screen.fill(BG)

        # Draw styled arrows with highlighting
        draw_arrow(screen, [(512, 90), (472, 160), (552, 160)], highlighted_command == "forward")   # Up
        draw_arrow(screen, [(512, 510), (472, 440), (552, 440)], highlighted_command == "backward") # Down
        draw_arrow(screen, [(272, 300), (342, 270), (342, 330)], highlighted_command == "left")     # Left
        draw_arrow(screen, [(752, 300), (682, 270), (682, 330)], highlighted_command == "right")    # Right

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                x, y = (event.x * screen.get_width(), event.y * screen.get_height()) if event.type == pygame.FINGERDOWN else event.pos
                if forward_rect.collidepoint(x, y):
                    move_forward()
                    highlighted_command = "forward"
                elif backward_rect.collidepoint(x, y):
                    move_backward()
                    highlighted_command = "backward"
                elif left_rect.collidepoint(x, y):
                    turn_left()
                    highlighted_command = "left"
                elif right_rect.collidepoint(x, y):
                    turn_right()
                    highlighted_command = "right"

            elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                stop_motors()
                highlighted_command = None

        time.sleep(0.01)

finally:
    stop_motors()
    GPIO.cleanup()
    pygame.quit()
    sys.exit()
