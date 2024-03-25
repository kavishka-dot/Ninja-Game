import sys
import pygame
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('ninja game') # display the name of the window
        self.screen = pygame.display.set_mode((640, 480)) # initilaize the screen size
        self.display = pygame.Surface((320,240)) # create a surface for future use

        self.clock = pygame.time.Clock() # initialize the clock speed

        self.movement = [False, False]

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player': load_image('entities/player.png')
        }

        self.player = PhysicsEntity(self, 'player', (50,50), (8,15))

        self.tilemap = TileMap(self)

    def run(self):
        while True:
            self.display.fill((14, 219,248))

            self.tilemap.render(self.display)

            self.player.update((self.movement[1] - self.movement[0], 0 ))
            self.player.render(self.display)
            
            # handle all the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # clicking the x
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()