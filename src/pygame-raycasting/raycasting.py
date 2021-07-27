import sys, pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

player_x = 50
player_y = 50

while True:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]: player_x -= 5
    if keys[pygame.K_RIGHT]: player_x += 5
    if keys[pygame.K_UP]: player_y -= 5
    if keys[pygame.K_DOWN]: player_y += 5
    
    win.fill((50,50,50))  # Fills the screen with black
    pygame.draw.rect(win, (0,255,0), (player_x, player_y, 5, 5))   
    pygame.display.update() 
    
pygame.quit()
