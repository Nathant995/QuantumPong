import pygame
from pygame.locals import *
import numpy as np
from qiskit import QuantumCircuit, Aer, execute


pygame.init()

# Set up the game window
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Quantum Pong")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
paddle_width = 10
paddle_height = 60
paddle_speed = 5
ball_radius = 10
ball_speed_x = 3
ball_speed_y = 3
max_velocity = 5

# Set up the quantum simulator -- If running on Qtm Hardware then comment the below out
simulator = Aer.get_backend('qasm_simulator')

# Quantum computation function
def quantum_computation():

    circ = QuantumCircuit(2, 2)

    circ.h(0)
    circ.cx(0, 1)
    angle = np.pi / 4
    circ.ry(angle, 1)
    circ.cx(1, 0)
    circ.measure(range(2), range(2))

    job = execute(circ, simulator, shots=1)
    result = job.result()
    counts = result.get_counts()

    # Process the measurement result for graphics and physics calculations
 
    measurement = list(counts.keys())[0]
    qubit_0 = int(measurement[1])  # Measurement result of qubit 0
    qubit_1 = int(measurement[0])  # Measurement result of qubit 1
    x_velocity = (qubit_0 - 0.5) * max_velocity
    y_velocity = (qubit_1 - 0.5) * max_velocity

    return x_velocity, y_velocity

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[K_UP] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[K_DOWN] and player_paddle.bottom < screen_height:
        player_paddle.y += paddle_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top < 0 or ball.bottom > screen_height:
        ball_speed_y *= -1
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

   
    if opponent_paddle.centery < ball.centery:
        opponent_paddle.y += paddle_speed
    else:
        opponent_paddle.y -= paddle_speed

    # Perform quantum computation for graphics and physics calculations
    x_velocity, y_velocity = quantum_computation()
    ball.x += x_velocity
    ball.y += y_velocity

    # Render graphics
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
