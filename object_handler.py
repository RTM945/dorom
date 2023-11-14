from sprite_object import *
from npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = os.path.join(base_path, "resources/sprites/doro")
        self.static_sprite_path = os.path.join(base_path, "resources/sprites/static_sprites/doro1.png")
        self.anim_sprite_path = os.path.join(base_path, "resources/sprites/animated_sprites/doro1.png")
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # add_sprite(SpriteObject(game))
        # add_sprite(AnimatedSprite(game))

        # add_npc(NPC(game))
        # add_npc(NPC(game, pos=(11.5, 4.5)))
        add_npc(NPC(game, pos=(11.0, 19.0)))
        add_npc(NPC(game, pos=(11.5, 4.5)))
        add_npc(NPC(game, pos=(13.5, 6.5)))
        add_npc(NPC(game, pos=(2.0, 20.0)))
        add_npc(NPC(game, pos=(4.0, 29.0)))
        add_npc(NPC(game, pos=(5.5, 14.5)))
        add_npc(NPC(game, pos=(5.5, 16.5)))
        add_npc(NPC(game, pos=(14.5, 25.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
    
    def add_npc(self, npc):
        self.npc_list.append(npc)