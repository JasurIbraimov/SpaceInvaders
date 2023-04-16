from animate import AnimatedSprite

class Player(AnimatedSprite):
    def __init__(self, filename):
        super().__init__(filename, scale=1)