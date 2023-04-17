import arcade 
import random
from constants import * 
from color import Color
from shape import Shape
from button import Button
from player import Player
from enemy import ShootingEnemy
from utils import *
from explosion import Explosion

class Game(arcade.Window):
    def __init__(self, title):
        super().__init__(title=title, fullscreen=True)
        self.set_mouse_visible(False)
  
        # Loading Background textures 
        self.bg = arcade.load_texture("assets/Backgrounds/black.png") 

        
        self.menu = True
        self.pause = False

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
        self.player_ships = arcade.SpriteList()
        self.main_player_ship = Player(3) 
        self.player_ships.append(self.main_player_ship)
        
        self.colors = arcade.SpriteList()
        self.shapes = arcade.SpriteList()
        self.lives = arcade.SpriteList()
        self.player_lasers = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.enemies_lasers = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.setup_colors()
        self.setup_shapes()
        self.setup_enemies()

        # Buttons
        self.choose_button = Button("CHOOSE", "assets/UI/button_blue.png", self.width/2, 100)
        self.pause_button = Button("MENU", "assets/UI/button_blue.png", self.width - 50, self.height - 80)
        self.resume_button = Button("RESUME", "assets/UI/button_blue.png", self.width/2, self.height/2+50)
        self.quit_button = Button("QUIT", "assets/UI/button_blue.png", self.width/2, self.height/2)
        
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
            live = arcade.Sprite(f"assets/Lives/player{self.main_player_ship.shape}_{self.main_player_ship.shape_color}.png", 1)
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

    def setup_enemies(self):
        """
            Method that creates enemies based on the level
        """
        for i in range(50):
            enemy = ShootingEnemy(self)
            enemy.set_position(random.randint(0, self.width), self.height + 100 * i)
            self.enemies.append(enemy)



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
            self.player_ships.draw()
            self.enemies.draw()
            self.enemies_lasers.draw()
            self.explosions.draw()
            self.player_lasers.draw()
            self.lives.draw()

        # Drawing pause button
        self.pause_button.draw()

        if self.pause:
            arcade.draw_rectangle_filled(
                self.width/2, 
                self.height/2, 
                300,
                250,
                arcade.color.WHITE
            )
            self.resume_button.draw()
            self.quit_button.draw()
        # Drawing cursor
        self.cursor.draw()

    def update(self, delta_time):
        if self.menu or self.pause: 
            return 
        self.player_lasers.update()
        self.enemies.update()
        self.enemies_lasers.update()
        self.explosions.update_animation()
        
        for enemy in self.enemies:
            if enemy.hp <= 0:
                explosion =  Explosion(enemy.center_x, enemy.center_y)
                self.explosions.append(explosion)
                enemy.kill()
        for laser in self.player_lasers:
            hits = arcade.check_for_collision_with_list(laser, self.enemies_lasers)
            if len(hits) > 0:
                laser.kill()
                for l in hits:
                    l.kill()
                    

    def on_mouse_motion(self, x, y, dx, dy):
        # To make cursor move with user mouse
        self.cursor.set_position(x, y)    
        if not self.menu and not self.pause:
            self.main_player_ship.center_x = x
        if len(self.player_ships) > 1:
            for i in range(1, len(self.player_ships)):
                if i % 2 == 0:  # for even i values, make center_x negative
                    center_x = self.main_player_ship.center_x - 100 * (i // 2)
                else:  # for odd i values, make center_x positive
                    center_x = self.main_player_ship.center_x + 100 * (i // 2 + 1)
                self.player_ships[i].center_x = center_x
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT: 
                # Handle click on Pause Button
            if check_item_clicked(x, y, self.pause_button):
                self.pause = True 

            if self.pause:
                # Handle click on Resume Button
                if check_item_clicked(x, y, self.resume_button):
                    self.pause = False 
                
                # Handle click on Quit Button
                if check_item_clicked(x, y, self.quit_button):
                    self.close()

            elif self.menu:
                # Choosing color
                for color in self.colors:
                    if check_item_clicked(x, y, color):
                        
                        # Reset all colors scales
                        for c in self.colors:
                            c.scale = COLOR_SCALE
                        
                        # Save chosen color
                        self.main_player_ship.shape_color = color.choose_color
                        
                        # Make chosen color bigger
                        color.scale = COLOR_CHOSEN_SCALE
                        
                        # Change buttons texture depending on chosen color 
                        button_texture = arcade.load_texture(f"assets/UI/button_{color.choose_color}.png")
                        self.choose_button.texture = button_texture
                        self.pause_button.texture = button_texture
                        self.resume_button.texture = button_texture
                        self.quit_button.texture = button_texture
                
                        # Change Shapes textures depending on chosen color 
                        for shape in self.shapes:
                            shape.texture = arcade.load_texture(f"assets/Player/player{shape.choose_shape}_{color.choose_color}.png")

                # Choosing Shape of SpaceShip
                for shape in self.shapes: 
                    if check_item_clicked(x, y, shape):

                        # Reset all shapes scales
                        for s in self.shapes:
                            s.scale = SHIP_SCALE

                        # Save chosen shape
                        self.main_player_ship.shape = shape.choose_shape

                        # Make chosen shape bigger
                        shape.scale = SHIP_CHOSEN_SCALE

                
                # Handle clicking to "Choose button"
                if check_item_clicked(x, y, self.choose_button):
                    self.menu = False # Turn off menu mode

                    # Creating player according to user choice
                    self.main_player_ship.change_shape()
                    self.setup_lives()
            else: 
                for player in self.player_ships:
                    player.shooting(self)
        
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.pause = not self.pause
        if symbol == arcade.key.NUM_1:
            for player in self.player_ships:
                player.shoot_mode = 1
        elif symbol == arcade.key.NUM_2:
            for player in self.player_ships:
                player.shoot_mode = 2
        elif symbol == arcade.key.NUM_3:
            for player in self.player_ships:
                player.shoot_mode = 3
        if symbol == arcade.key.C:
            for player in self.player_ships:
                player.laser_type = "common"
        if symbol == arcade.key.P:
            for player in self.player_ships:
                player.laser_type = "penetrate"
        if symbol == arcade.key.R:
            for player in self.player_ships:
                player.laser_type = "ricochet"
        if symbol == arcade.key.H:
            for player in self.player_ships:
                player.laser_type = "horming"
        if symbol == arcade.key.A:
            player = Player(1, self.main_player_ship.shape, self.main_player_ship.shape_color)
            player.center_x = self.main_player_ship.center_x
            self.player_ships.append(player)
        
window = Game(SCREEN_TITLE)
arcade.run()