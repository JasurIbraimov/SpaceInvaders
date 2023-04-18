import arcade 
import random
from time import time
from constants import * 
from color import Color
from shape import Shape
from button import Button
from player import Player
from enemy import ShootingEnemy, Enemy
from utils import *
from explosion import Explosion

class Game(arcade.Window):
    def __init__(self, title):
        super().__init__(title=title, fullscreen=True)
        self.set_mouse_visible(False)
  
        # Loading Background textures 
        self.bg = arcade.load_texture("assets/Backgrounds/black.png") 
        self.planet = arcade.load_texture("assets/Backgrounds/planet.png")
        
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

        self.start_timer_text = arcade.Text(
            "3",
            self.width/2, 
            self.height/2, 
            font_size=75,
            font_name="kenvector future"
        )

        self.score_text = arcade.Text(
            "SCORE: 0",
            self.width - 170, 
            self.height-150, 
            font_size=18,
            font_name="kenvector future"
        )

        self.level_text = arcade.Text(
            "LEVEL: 1",
            50, 
            self.height - 50, 
            font_size=18,
            font_name="kenvector future"
        )
        self.game_over_text = arcade.Text( 
            "GAME OVER",
            self.width/4, 
            self.height/2, 
            font_size=75,
            font_name="kenvector future"
        )
        # Start Timer
        self.start_timer = time()
        self.start_countdown = 3
        self.start = False
        
        # Game Over
        self.game_over = False 
        # Player score
        self.score = 0
        
        # SpriteLists 
        self.player_ships = arcade.SpriteList()
        self.main_player_ship = Player(3, self) 
        self.player_ships.append(self.main_player_ship)
        
        self.colors = arcade.SpriteList()
        self.shapes = arcade.SpriteList()
        self.lives = arcade.SpriteList()
        self.player_lasers = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.enemies_lasers = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.power_ups = arcade.SpriteList()
        self.setup_colors()
        self.setup_shapes()

        # Buttons
        self.choose_button = Button("CHOOSE", "assets/UI/button_blue.png", self.width/2, 100)
        self.pause_button = Button("MENU", "assets/UI/button_blue.png", self.width - 50, 100)
        self.resume_button = Button("RESUME", "assets/UI/button_blue.png", self.width/2, self.height/2+50)
        self.quit_button = Button("QUIT", "assets/UI/button_blue.png", self.width/2, self.height/2)
        self.restart_button = Button("RESTART", "assets/UI/button_blue.png", self.width/2, self.height/2 - 100)

        self.level = 1
        
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
            live.set_position(self.width - 150 + 60 * i, self.height-100)
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

    def setup_common_enemies(self, hp, enemy_count, enemy_speed=ENEMY_SPEED):
        """
            Method that creates common enemies 
        """
        for i in range(enemy_count):
            enemy = Enemy(hp, self)
            enemy.change_y = enemy_speed
            enemy.center_y = self.height + 100 * i
            self.enemies.append(enemy)

    def setup_shooting_enemies(self, hp, enemy_count, laser_type="common", shooting_speed=ENEMY_SHOOTING_TIMER):
        """
            Method that creates shooting enemies 
        """
        for i in range(enemy_count):
            if isinstance(laser_type, tuple): 
                laser = random.choice(laser_type)
            else:
                laser = laser_type
            enemy = ShootingEnemy(hp, self, laser, shooting_speed)
            enemy.center_y = self.height + 100 * i
            self.enemies.append(enemy)

    def setup_levels(self):
        """
            Method that creates levels
        """
        if self.level == 1: 
            self.setup_common_enemies(1, 25)
        elif self.level == 2:
            self.setup_common_enemies(2, 25, ENEMY_SPEED + 0.2)
        elif self.level == 3:
            self.setup_shooting_enemies(3, 25, "common")
        elif self.level == 4: 
            self.setup_shooting_enemies(4, 30, "ricochet")
        elif self.level == 5:
            self.setup_shooting_enemies(5, 40, "horming", ENEMY_SHOOTING_TIMER - 0.5)
        elif self.level == 6:
            self.setup_shooting_enemies( 6, 40, ("horming", "ricochet", "common"), ENEMY_SHOOTING_TIMER - 1)
        elif self.level == 7: 
            self.setup_common_enemies(8, 40, ENEMY_SPEED + 0.5)
            self.setup_shooting_enemies(8, 10, ("horming", "ricochet", "common"), ENEMY_SHOOTING_TIMER - 1.5)

    def setup_countdown_timer(self):
        self.start = False
        self.start_countdown = 3
        self.start_timer_text.text = self.start_countdown
        self.start_timer = time()
    
    def on_draw(self):
        # Drawing background of the game
        arcade.draw_texture_rectangle(
            self.width/2, 
            self.height/2, 
            self.width,  
            self.height,
            self.bg
        )
        arcade.draw_texture_rectangle(
            self.width/2, 
            -self.height/3, 
            self.planet.width,  
            self.planet.height,
            self.planet
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
             # Player shop 
            arcade.draw_rectangle_filled(
                self.width - 75, 
                self.height/2, 
                100,  
                500,
                arcade.color.DARK_BLUE_GRAY
            )
            # Player score 
            self.score_text.draw()
            # Level 
            self.level_text.draw()

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
        if self.game_over:
            self.game_over_text.draw()
            self.restart_button.draw()
        if not self.pause and not self.menu and not self.start:
            self.start_timer_text.draw()
        # Drawing cursor
        self.cursor.draw()

    def update(self, delta_time):
        if self.menu or self.pause or self.game_over: 
            return 

        if not self.start:
            if time() - self.start_timer > 1 :
                self.start_countdown = self.start_countdown - 1
                self.start_timer = time()
                self.start_timer_text.text = self.start_countdown
            if self.start_countdown == 0:
                self.start = True
            return
        self.player_lasers.update()
        self.enemies.update()
        self.enemies_lasers.update()
        self.explosions.update_animation()

        if len(self.enemies) == 0:
            self.level = self.level + 1
            self.setup_levels()
            self.level_text.text = f"LEVEL: {self.level}"
            return
        
        # if any of enemies are destoyed create an explosion after them
        for enemy in self.enemies:
            if enemy.hp <= 0:
                explosion =  Explosion(enemy.center_x, enemy.center_y)
                self.explosions.append(explosion)
                enemy.kill()
                # Increase score by 1 and change score text on the screen
                self.score = self.score + 1
                self.score_text.text = f"SCORE: {self.score}"

        # Check if player lasers collide with enemy lasers 
        for laser in self.enemies_lasers:
            hits = arcade.check_for_collision_with_list(laser, self.player_lasers)
            if len(hits) > 0:
                laser.kill()
                for l in hits:
                    l.kill()
        if self.main_player_ship.hp == 0:
            self.start = False 
            self.game_over = True 

            
                    
    def on_mouse_motion(self, x, y, dx, dy):
        # To make cursor move with user mouse
        self.cursor.set_position(x, y)  

        # Move user's ship to ther cursor position x  
        if not self.menu and not self.pause and self.start and x < self.width-200:
            self.main_player_ship.center_x = x
        
        # If user have more than 1 ship
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
            if check_item_clicked(x, y, self.restart_button) and self.game_over:
                self.game_over = False
                self.menu = True
                self.setup_lives()
                self.main_player_ship.hp = 3
                self.enemies.clear()
                self.player_lasers.clear()
                self.enemies_lasers.clear()
                self.level = 1
                self.level_text.text = f"LEVEL: {self.level}"
                self.score = 0
                self.score_text.text = f"SCORE: {self.score}"
                self.setup_levels()

            if self.pause:
                # Handle click on Resume Button
                if check_item_clicked(x, y, self.resume_button):
                    self.pause = False 
                    self.setup_countdown_timer()
                
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
                    self.setup_levels()
                    self.start_timer = time()
                    # Creating player according to user choice
                    self.main_player_ship.change_shape()
                    self.main_player_ship.center_x = self.width/2
                    self.setup_lives()
            else: 
                if self.start:
                    for player in self.player_ships:
                        player.shooting()
        
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.pause = not self.pause
            if not self.pause:
                self.setup_countdown_timer()

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
            player = Player(1, self, self.main_player_ship.shape, self.main_player_ship.shape_color)
            player.center_x = self.main_player_ship.center_x
            self.player_ships.append(player)
        
window = Game(SCREEN_TITLE)
arcade.run()