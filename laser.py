from arcade import Sprite, check_for_collision_with_list
import constants as C

class Laser(Sprite):
    """
        Base Laser Class
    """
    def __init__(self, color, laser_type, speed, damage, enemies):
        super().__init__(f"assets/Lasers/laser_{color}_{laser_type}.png", scale=1)
        self.damage = damage
        self.change_y = speed
        self.enemies = enemies
    def update(self):
        self.center_y = self.center_y + self.change_y   # just go up 

    def check_collision_with_enemies(self):
        # Check if collides with enemies
        hits = check_for_collision_with_list(self, self.enemies)
        if len(hits) > 0:
            for enemy in hits: 
                enemy.hp -= self.damage
            return True 

class CommonLaser(Laser):
    """
        Common Laser Class
    """
    def __init__(self, color, enemies):
        super().__init__(color, "common", C.COMMON_LASER_SPEED, C.COMMON_LASER_DAMAGE, enemies)

    def update(self):
        super().update()
        if self.bottom >= self.boundary_top or self.check_collision_with_enemies(): # if above the screen kill the sprite
            self.kill() 
        

class RicochetLaser(Laser):
    """
        Ricochet Laser Class
    """
    def __init__(self, color, enemies):
        super().__init__(color, "ricochet", C.RICHOCHET_LASER_SPEED, C.RICHOCHET_LASER_DAMAGE, enemies)
        self.ricochet_times = 0
    
    def update(self):
        super().update()
        self.angle += C.RICHOCHET_ROTATION_SPEED
        if self.bottom <= 0 or self.top >= self.boundary_top or self.check_collision_with_enemies():  # if collides with screen borders
            self.ricochet()

        if self.ricochet_times >= 5: # if ricochet count >= 5 kill the sprite
            self.kill()

    def ricochet(self):
        self.change_y=-self.change_y # ricochet 
        self.ricochet_times += 1 # increase ricochet count by 1



class PenetrateLaser(Laser):
    """
        Penetrate Laser Class
    """
    def __init__(self, color, enemies):
        super().__init__(color, "penetrate", C.PENETRATE_LASER_SPEED, C.PENETRATE_LASER_DAMAGE, enemies)
        self.change_scale = C.PENETRATE_PULSE_SPEED
    def update(self):
        super().update()
        self.pulse()
        self.check_collision_with_enemies()
        if self.bottom >= self.boundary_top: # if above the screen kill the sprite
            self.kill() 
    def pulse(self):
        self.scale += self.change_scale
        if self.scale >= 1.5 or self.scale <= 1:
            self.change_scale = -self.change_scale
        
