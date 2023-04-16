from animate import AnimatedSprite
from laser import RicochetLaser, PenetrateLaser, CommonLaser
from arcade import load_texture
class Player(AnimatedSprite):
    def __init__(self, shape="Ship1", color="blue"):
        super().__init__(f"assets/Player/player{shape}_{color}.png", scale=0.8)
        self.shoot_mode = 3
        self.shape = shape 
        self.shape_color = color
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
            laser = CommonLaser(self.shape_color, window.enemies)
        elif self.laser_type == "ricochet":
            laser = RicochetLaser(self.shape_color, window.enemies)
        else:
            laser = PenetrateLaser(self.shape_color, window.enemies)
        laser.set_position(x, self.top)
        laser.boundary_top = window.height
        window.lasers.append(laser)
        laser.scale = scale
    
    def common_shooting(self, window):
        self.create_laser(1, self.center_x, window)
    
    def double_shooting(self, window):
        self.create_laser(0.8, self.center_x - 30, window) 
        self.create_laser(0.8, self.center_x + 30, window)

    def triple_shooting(self, window):        
        self.common_shooting(window)
        self.double_shooting(window)