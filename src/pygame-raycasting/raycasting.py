# packages
import sys
import pygame
import math

# init pygame
pygame.init()
clock = pygame.time.Clock()

# map (MAP_SIZE x MAP_SIZE)
MAP = (
    '########'
    '#  #   #'
    '#  ##  #'
    '#      #'
    '###  # #'
    '#    # #'
    '#    # #'
    '########'
)

# global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
CASTED_RAYS = 60
MAP_SIZE = 8
TILE_SIZE = SCREEN_HEIGHT / MAP_SIZE
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FIELD_OF_VIEW = math.pi / 3
STEP_ANGLE = FIELD_OF_VIEW / CASTED_RAYS

SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS
HALF_HEIGHT = SCREEN_HEIGHT / 2
PROJ_COEFF = 3 * CASTED_RAYS / (2 * math.tan(FIELD_OF_VIEW / 2)) * TILE_SIZE

# global variables
player_x = SCREEN_HEIGHT / 2
player_y = SCREEN_HEIGHT / 2
player_angle = math.pi

# create window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ray casting")

# draw map
def draw_map():
    # draw map background
    pygame.draw.rect(win, (50, 50, 50), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))
    
    # loop over map rows
    for row in range(8):
        # loop over map colums
        for col in range(8):
            # convert row & col ti map square index
            square = row * MAP_SIZE + col
            
            # draw rectangle if find 'wall' at map square index
            pygame.draw.rect(win, (200, 200, 200) if MAP[square] == '#' else (100, 100, 100),
                            (col * TILE_SIZE,
                             row * TILE_SIZE,
                             TILE_SIZE-2,
                             TILE_SIZE-2))
        
    # draw player
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)

# ray casting algorithm
def cast_rays():
    # define initial angle
    start_angle = player_angle - FIELD_OF_VIEW / 2
    
    # loop over casting rays (used screen width pixels)
    for ray in range(CASTED_RAYS):
        # cast ray
        for depth in range(MAX_DEPTH):
            # extend ray
            target_x = player_x + depth * math.sin(start_angle)
            target_y = player_y + depth * math.cos(start_angle)
            
            # ray hits the wall
            if MAP[int(target_y / TILE_SIZE) * MAP_SIZE + int(target_x / TILE_SIZE)] == '#':
                # highlight the wall
                target_col = int(target_x / TILE_SIZE)
                target_row = int(target_y / TILE_SIZE)
                pygame.draw.rect(win, (0, 255, 0), (target_col * TILE_SIZE,
                                                    target_row * TILE_SIZE,
                                                    TILE_SIZE - 2,
                                                    TILE_SIZE - 2))
                # drop casting ray
                break
            
            # draw casting ray
            pygame.draw.line(win, (255, 255, 0), (player_x, player_y), (target_x, target_y))
            
            ######################
            # draw 3D projection
            ######################
            
            # fix fish eye view
            depth *= math.cos(player_angle - start_angle)
            proj_height = min(PROJ_COEFF / (depth + 0.0001), SCREEN_HEIGHT)
            c = 255 / (1 + depth * depth * 0.0001)
            color = (c / 2, c, c / 3)
            pygame.draw.rect(win, color, (480 + ray * SCALE, HALF_HEIGHT - proj_height / 2, SCALE, proj_height))

        # increment angle
        start_angle += STEP_ANGLE    

# moving direction
forward = True

# game loop
while True:    
    # escpare condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    
    # draw 2D map
    draw_map()
    
    # render scene
    cast_rays()
            
    # get user input
    keys = pygame.key.get_pressed()
    
    # collision detection
    if MAP[int(player_y / TILE_SIZE) * MAP_SIZE + int(player_x / TILE_SIZE)] == '#':
        # highlight the wall
        target_col = int(player_x / TILE_SIZE)
        target_row = int(player_y / TILE_SIZE)
        pygame.draw.rect(win, (255, 0, 0), (target_col * TILE_SIZE,
                                            target_row * TILE_SIZE,
                                            TILE_SIZE - 2,
                                            TILE_SIZE - 2))

        # drop back
        if forward:
            player_x -= 5 * math.sin(player_angle)
            player_y -= 5 * math.cos(player_angle)
        
        else:
            player_x += 5 * math.sin(player_angle)
            player_y += 5 * math.cos(player_angle)

    # update player position/view
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        player_x += 5 * math.sin(player_angle)
        player_y += 5 * math.cos(player_angle)
        forward = True
        
    if keys[pygame.K_DOWN]:
        player_x -= 5 * math.sin(player_angle)
        player_y -= 5 * math.cos(player_angle)
        forward = False

    # update frame according to FPS
    pygame.display.flip()
    clock.tick(60)

# clean ups
pygame.quit()
