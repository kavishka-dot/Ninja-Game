import sys
import pygame
from scripts.utils import load_images
from scripts.tilemap import TileMap

RENDER_SCLAE = 2.0

class Editor:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('editor') # display the name of the window
        self.screen = pygame.display.set_mode((640, 480)) # initilaize the screen size
        self.display = pygame.Surface((320,240)) # create a surface for future use

        self.clock = pygame.time.Clock() # initialize the clock speed

        


        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners')

        }
        self.tilemap = TileMap(self)

        self.movement = [False, False, False, False]

        try:
            self.tilemap.load('map.json')
            print("Got it")
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
    def run(self):
        while True:
            self.display.fill((0,0,0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset = render_scroll)


            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()

            mpos = (mpos[0]/ RENDER_SCLAE, mpos[1]/ RENDER_SCLAE)

            tile_pos = (int((mpos[0] + self.scroll[0])//self.tilemap.tile_size), int((mpos[1] + self.scroll[1])//self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size- self.scroll[0], tile_pos[1] * self.tilemap.tile_size- self.scroll[1] ))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tile_map[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type' : self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tile_map:
                    del(self.tilemap.tile_map[tile_loc])
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            
            self.display.blit(current_tile_img, (5,5))

            
            # handle all the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # clicking the x
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # left clicking
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append( {'type' : self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant-1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant+1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group-1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group+1) % len(self.tile_list)
                            self.tile_variant = 0 
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # left clicking
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                    
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()