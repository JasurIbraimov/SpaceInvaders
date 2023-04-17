from animate import AnimatedSprite
from laser import RicochetLaser, PenetrateLaser, CommonLaser, HormingLaser
from arcade import load_texture
import constants as C

class Player(AnimatedSprite):
    def __init__(self, hp, shape="Ship1", color="blue"):
        super().__init__(f"assets/Player/player{shape}_{color}.png", scale=0.8)
        self.center_y = 100
        self.shoot_mode = 3
        self.shape = shape 
        self.shape_color = color
        self.hp = hp
        self.laser_type = "common"
 
    def change_shape(self):
        self.texture = load_texture(f"assets/Player/player{self.shape}_{self.shape_color}.png")

    def shooting(self, window):
        if self.shoot_mode == 1:
            self.common_shooting(window)
        elif self.shoot_mode == 2:
            self.double_shooting(window)
        else:
            self.triple_shooting(window)

    def create_laser(self, scale, x, window):
        if self.laser_type == "common":
            laser = CommonLaser(self.shape_color, window.enemies, C.COMMON_LASER_SPEED, C.COMMON_LASER_DAMAGE, window.height)
        elif self.laser_type == "ricochet":
            laser = RicochetLaser(self.shape_color, window.enemies, C.RICHOCHET_LASER_SPEED, C.RICHOCHET_LASER_DAMAGE, window.height)
        elif self.laser_type == "penetrate":
            laser = PenetrateLaser(self.shape_color, window.enemies, C.PENETRATE_LASER_SPEED, C.PENETRATE_LASER_DAMAGE, scale, window.height)
        else: 
            laser = HormingLaser(self.shape_color, window.enemies, C.HORMING_LASER_SPEED, 1, window.height)
        laser.set_position(x, self.top)
        window.player_lasers.append(laser)
        laser.scale = scale
    
    def common_shooting(self, window):
        self.create_laser(1, self.center_x, window)
    
    def double_shooting(self, window):
        self.create_laser(0.8, self.center_x - 30, window) 
        self.create_laser(0.8, self.center_x + 30, window)

    def triple_shooting(self, window):        
        self.common_shooting(window)
        self.double_shooting(window)