import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}  # looking for a value in a set is much faster

class TileMap:

    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.offgrid_tiles = []
        
        for i in range(10):
            self.tile_map[str(3+i) + ';10'] = {'type':'grass', 'variant': 1, 'pos': (3+i, 10)}
            self.tile_map['10;' + str(5+i)] = {'type':'stone', 'variant': 1, 'pos': (10, 5+i)} # position is given in terms of tiles

    def tiles_around(self, pos):
        '''Returns tiles where tiles are availabel around the player'''
        tiles = []
        tile_loc = (int(pos[0]//self.tile_size),int(pos[1]//self.tile_size))

        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        '''Seperates tiles which are physics enabled and creates rects around them'''
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects


    def render(self, surf,offset = (0,0)):

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            pass

        # for tile in self.offgrid_tiles: # we must render the offgrid before tile_map
        #     surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1]-offset[1]) )
        
        for loc in self.tile_map: # iterates through all the tiles
            tile = self.tile_map[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))


        