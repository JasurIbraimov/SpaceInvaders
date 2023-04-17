from arcade import Sprite 
from random import randint, choice
from time import time
from laser import CommonLaser, RicochetLaser, HormingLaser
import constants as C

class Enemy(Sprite):
    def __init__(self, hp, window):
        colors = ["blue", "green", "red"]
        self.shape_color = choice(colors)
        super().__init__(f"assets/Enemies/enemy_{self.shape_color}{randint(1, 5)}.png", 1)
        self.change_y = 1
        self.hp = hp
        self.window = window
    def update(self):
        self.center_y-= self.change_y
        if self.top <= 0:
            self.kill()


class ShootingEnemy(Enemy):
    def __init__(self, window):
        super().__init__(5, window)
        self.shooting_time = time()
    
    def update(self):
        super().update()
        if self.top <= self.window.height:
            if time() - self.shooting_time >= 5: 
                self.shoot()
    
    def shoot(self):
        laser = HormingLaser(self.shape_color, self.window.player_ships, C.HORMING_LASER_SPEED, 1, self.window.height)
        laser.set_position(self.center_x, self.bottom)
        self.window.enemies_lasers.append(laser)
        self.shooting_time = time()