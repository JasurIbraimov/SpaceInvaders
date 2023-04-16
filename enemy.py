from arcade import Sprite 


class Enemy(Sprite):
    def __init__(self, hp):
        super().__init__("assets/Enemies/enemyRed1.png", 1)
        self.change_y = 1
        self.hp = hp
    def update(self):
        self.center_y-= self.change_y
        if self.top <= 0:
            self.kill()
        if self.hp <= 0:
            self.kill()