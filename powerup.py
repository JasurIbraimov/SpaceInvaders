from arcade import Sprite, Text


class PowerUp(Sprite):
    def __init__(self, filename, cost, name, cx, cy):
        super().__init__(filename, 1.5)
        self.cost = cost 
        self.set_position(cx, cy)
        self.name = name
        self.cost_text = Text(str(self.cost),  self.center_x-15, self.bottom-10, font_size=16, font_name="kenvector future")
    
    def draw(self):
        super().draw()
        self.cost_text.draw()
        
