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
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(100)
    pwm_ENB.ChangeDutyCycle(100)

def turn_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(100)
    pwm_ENB.ChangeDutyCycle(100)

def turn_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
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

# Colors
BLACK = (0, 0, 0)
BLUE = (50, 120, 255)
LIGHT_BLUE = (100, 180, 255)

# Define arrow zones
forward_rect = pygame.Rect(462, 80, 100, 100)
left_rect = pygame.Rect(262, 250, 100, 100)
right_rect = pygame.Rect(662, 250, 100, 100)

highlighted_command = None

def draw_arrow(surface, points, is_highlighted):
    color = LIGHT_BLUE if is_highlighted else BLUE
    pygame.draw.polygon(surface, color, points)

running = True

try:
    clock = pygame.time.Clock()
    while running:
        screen.fill(BLACK)

        # Draw arrows (only color changes slightly if highlighted)
        draw_arrow(screen, 
                   [(forward_rect.centerx, forward_rect.top + 10),
                    (forward_rect.left + 10, forward_rect.bottom - 10),
                    (forward_rect.right - 10, forward_rect.bottom - 10)], 
                   highlighted_command == "forward")

        draw_arrow(screen, 
                   [(left_rect.left + 10, left_rect.centery),
                    (left_rect.right - 10, left_rect.top + 10),
                    (left_rect.right - 10, left_rect.bottom - 10)], 
                   highlighted_command == "left")

        draw_arrow(screen, 
                   [(right_rect.right - 10, right_rect.centery),
                    (right_rect.left + 10, right_rect.top + 10),
                    (right_rect.left + 10, right_rect.bottom - 10)], 
                   highlighted_command == "right")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                x, y = (event.x * screen.get_width(), event.y * screen.get_height()) if event.type == pygame.FINGERDOWN else event.pos
                if forward_rect.collidepoint(x, y):
                    move_forward()
                    highlighted_command = "forward"
                elif left_rect.collidepoint(x, y):
                    turn_left()
                    highlighted_command = "left"
                elif right_rect.collidepoint(x, y):
                    turn_right()
                    highlighted_command = "right"

            elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                stop_motors()
                highlighted_command = None

        clock.tick(60)

finally:
    stop_motors()
    GPIO.cleanup()
    pygame.quit()
    sys.exit()
