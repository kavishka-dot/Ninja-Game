import pygame
import json

AUTOTILE_MAP = {
     tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8

}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}  # looking for a value in a set is much faster
AUTOTILE_TYPES = {'grass', 'stone'}

class TileMap:

    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep = False):
        matches = []

        # for offgrid tiles
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        
        # for grid tiles
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()

                # turn the grid positions to pixel positions
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tile_map[loc]

        return matches

    def tiles_around(self, pos):
        '''Returns tiles where tiles are availabel around the player'''
        tiles = []
        tile_loc = (int(pos[0]//self.tile_size),int(pos[1]//self.tile_size))

        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tile_map:
                tiles.append(self.tile_map[check_loc])
        return tiles
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tile_map, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()

    def load(self,path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tile_map = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def physics_rects_around(self, pos):
        '''Seperates tiles which are physics enabled and creates rects around them'''
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for loc in self.tile_map:
            tile = self.tile_map[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tile_map:
                    if self.tile_map[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]




    def render(self, surf,offset = (0,0)):
        for tile in self.offgrid_tiles: # we must render the offgrid before tile_map
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1]-offset[1]) )

        # iterates through the tiles which should be rendered. Improves the efficiency
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tile_map:
                    tile = self.tile_map[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
            

        