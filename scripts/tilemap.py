class TileMap:

    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.tile_map = {}
        self.offgrid_tiles = []
        
        for i in range(10):
            self.tile_map[str(3+i) + ';10'] = {'type':'grass', 'variant': 1, 'pos': (3+i, 10)}
            self.tile_map['10;' + str(i+5)] = {'type':'stone', 'variant': 1, 'pos': (10, i+5)} # position is given in terms of tiles

    def render(self, surf):

        for tile in self.offgrid_tiles: # we must render the offgrid before tile_map
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'] )
        
        for loc in self.tile_map: # iterates through all the tiles
            tile = self.tile_map[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))


        