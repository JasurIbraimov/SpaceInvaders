from arcade import Sprite, Text, load_texture, draw_texture_rectangle
from arcade.color import GRAY


class PowerUp(Sprite):
    def __init__(self, filename, cost, name, cx, cy):
        super().__init__(filename, 1.5)
        self.cost = cost 
        self.set_position(cx, cy)
        self.name = name
        self.opened = False
        self.locked_texture = load_texture("assets/UI/lock.png")
        self.cost_text = Text(str(self.cost),  self.center_x-15, self.bottom-10, font_size=16, font_name="kenvector future")
        self.color = GRAY

    def draw(self):
        super().draw()
        self.cost_text.draw()
        if not self.opened:
            draw_texture_rectangle(self.center_x, self.center_y, self.locked_texture.width/4, self.locked_texture.height/4, self.locked_texture)
            
        
