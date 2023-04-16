import arcade 
from constants import * 
from color import Color
from shape import Shape
from button import Button
from player import Player

class Game(arcade.Window):
    def __init__(self, title):
        super().__init__(title=title, fullscreen=True)
        self.set_mouse_visible(False)
        self.chosen_color = "blue"
        self.chosen_shape = "Ship1"
        
        # Loading Background textures 
        self.bg = arcade.load_texture("assets/Backgrounds/black.png") 

        
        self.menu = True
        self.player = None 

        # Loading Custom Font
        arcade.load_font("assets/Font/kenvector_future.ttf")
        self.cursor = arcade.Sprite("assets/UI/cursor.png")
        

        # Texts
        self.choose_text = arcade.Text(
            "Choose you spaceship!", 
            self.width/5, 
            self.height - 100,
            font_size=50, 
            font_name="kenvector future"
        )

        self.color_text = arcade.Text(
            "Color",
            self.width/5,
            self.height/2,
            font_size=28,
            font_name="kenvector future"
        )

        self.shape_text = arcade.Text(
            "Shape",
            self.width/5,
            self.height/2 - 200,
            font_size=28,
            font_name="kenvector future"
        )



        # SpriteLists 
        self.colors = arcade.SpriteList()
        self.shapes = arcade.SpriteList()
        self.lives = arcade.SpriteList()
        self.setup_colors()
        self.setup_shapes()

        # Buttons
        self.choose_button = Button("CHOOSE", "assets/UI/button_blue.png", self.width/2, 100)
    def setup_colors(self):
        """
            Method that creates colors on the screen, and places them
        """
        blue = Color("assets/UI/dotBlue.png", "blue")
        blue.scale = COLOR_CHOSEN_SCALE
        green = Color("assets/UI/dotGreen.png", "green")
        red = Color("assets/UI/dotRed.png", "red")
        blue.set_position(self.width/2, self.height/2 + 20)
        green.set_position(self.width/2 + 100, self.height/2 + 20)
        red.set_position(self.width/2 + 200, self.height/2 + 20)
        self.colors.append(blue)
        self.colors.append(green)
        self.colors.append(red)

    def setup_lives(self):
        """
            Method that creates lives of player, according to shape and color
        """
        for i in range(3):
            live = arcade.Sprite(f"assets/Lives/player{self.chosen_shape}_{self.chosen_color}.png", 1)
            live.set_position(200 + 60 * i, self.height - 50)
            self.lives.append(live) 


    def setup_shapes(self):
        """
            Method that creates shapes on the screen, and places them
        """
        for i in range(1, 5):
            shape = Shape(f"assets/Player/playerShip{i}_blue.png", f"Ship{i}")
            shape.set_position(self.width/3 + 180 * i, self.height/2 - 200 + 20)
            self.shapes.append(shape)
        self.shapes[0].scale = SHIP_CHOSEN_SCALE

    def on_draw(self):
        # Drawing background of the game
        arcade.draw_texture_rectangle(
            self.width/2, 
            self.height/2, 
            self.width,  
            self.height,
            self.bg
        )
        if self.menu: # in menu mode
            self.choose_text.draw()
            self.color_text.draw()
            self.colors.draw()
            self.shape_text.draw()
            self.shapes.draw()
            self.choose_button.draw()
        else:
            self.player.draw()
            self.lives.draw()
        # Drawing cursor
        self.cursor.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # To make cursor move with user mouse
        self.cursor.set_position(x, y)    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT: 
            if self.menu:
                # Choosing color
                for color in self.colors:
                    if color.left<=x<=color.right and color.bottom<=y<=color.top:
                        
                        # Reset all colors scales
                        for c in self.colors:
                            c.scale = COLOR_SCALE
                        
                        # Save chosen color
                        self.chosen_color = color.choose_color
                        
                        # Make chosen color bigger
                        color.scale = COLOR_CHOSEN_SCALE
                        
                        # Change "Choose button" texture depending on chosen color 
                        self.choose_button.texture = arcade.load_texture(f"assets/UI/button_{color.choose_color}.png")
                        
                        # Change Shapes textures depending on chosen color 
                        for shape in self.shapes:
                            shape.texture = arcade.load_texture(f"assets/Player/player{shape.choose_shape}_{color.choose_color}.png")

                # Choosing Shape of SpaceShip
                for shape in self.shapes: 
                    if shape.left<=x<=shape.right and shape.bottom<=y<=shape.top:

                        # Reset all shapes scales
                        for s in self.shapes:
                            s.scale = SHIP_SCALE

                        # Save chosen shape
                        self.chosen_shape = shape.choose_shape

                        # Make chosen shape bigger
                        shape.scale = SHIP_CHOSEN_SCALE

                
                # Handle clicking to "Choose button"
                if self.choose_button.left <= x <= self.choose_button.right  and self.choose_button.bottom <= y <= self.choose_button.top:
                    self.menu = False # Turn off menu mode

                    # Creating player according to user choice
                    self.player = Player(f"assets/Player/player{self.chosen_shape}_{self.chosen_color}.png")
                    self.player.set_position(self.width/2, 100)
                    self.setup_lives()
                 
window = Game(SCREEN_TITLE)
arcade.run()