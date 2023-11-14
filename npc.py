from sprite_object import *
from random import randint, random

class NPC(AnimatedSprite):
    def __init__(self, game, path=os.path.join(base_path, "resources/sprites/animated_sprites/doro1.png"),
                 pos=(11.5, 3.5), scale = 0.5, shift=0.6, animation_time=randint(100, 120)):
        super().__init__(game, path, pos, scale, shift, animation_time)
        
        self.speed = 0.03
        self.size = 40
        self.ray_cast_value = False
        self.attack_dist = randint(3, 6)
        self.player_search_trigger = False

        self.idle_images = self.get_images(os.path.join(base_path, "resources/sprites/doro/idle"))
        self.walk_images = self.get_images(os.path.join(base_path, "resources/sprites/doro/walk"))

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def run_logic(self):
        self.ray_cast_value = self.ray_cast_player_npc()
        if self.ray_cast_value:
            self.player_search_trigger = True
            if self.dist < self.attack_dist:
                self.animate(self.idle_images)
            else:
                self.animate(self.walk_images)
                self.movement()
        elif self.player_search_trigger:
            self.animate(self.walk_images)
            self.movement()
        else:
            self.animate(self.idle_images)
        

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
    
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False