from arcade import Sprite, draw_rectangle_filled, draw_rectangle_outline
from random import randint, choice
from time import time
from laser import CommonLaser, RicochetLaser, HormingLaser
import constants as C

class Enemy(Sprite):
    def __init__(self, hp, window, shape=1):
        colors = ["blue", "green", "red"]
        # random enemy color can't be color of ther user
        colors.remove(window.main_player_ship.shape_color)
        self.shape_color = choice(colors) 
        super().__init__(f"assets/Enemies/enemy_{self.shape_color}{shape}.png", 1)
        self.window = window
        self.center_x = randint(0 + self.width//2, self.window.width - self.width//2)
        self.change_y = C.ENEMY_SPEED
        self.hp = hp
        
    def update(self):
        self.center_y-= self.change_y
        if self.top <= 0:
            self.kill()


class ShootingEnemy(Enemy):
    def __init__(self, hp, window, laser_type, shooting_speed):
        if laser_type == "common": 
            shape = 2
        elif laser_type == "ricochet":
            shape = 3
        elif laser_type == "horming":
            shape = 4
        super().__init__(hp, window, shape, )
        self.shooting_time = time()
        self.laser_type = laser_type
        self.shooting_speed = shooting_speed
    
    def update(self):
        super().update()
        if self.top <= self.window.height:
            if time() - self.shooting_time >= self.shooting_speed: 
                self.shoot()
    
    def shoot(self):
        """
            Method that creates laser for enemy
        """
        params = (self.shape_color, self.window.player_ships, 1, self.window.height)
        if self.laser_type == "common": 
            laser = CommonLaser(*params, -C.COMMON_LASER_SPEED)
        elif self.laser_type == "horming":
            laser = HormingLaser(*params, C.HORMING_LASER_SPEED)
        else: 
            laser = RicochetLaser(*params, -C.RICHOCHET_LASER_SPEED)
        laser.set_position(self.center_x, self.bottom)
        self.window.enemies_lasers.append(laser)
        self.shooting_time = time()