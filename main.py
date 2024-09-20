"""
Find Me Game
"""
import arcade

import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Find Me"

TILE_SCALING = 0.2


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        # Background image will be stored in this variable
        self.background = None

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.items_list = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.background = arcade.load_texture("./img/background/forest1.jpg")

        # Create the Sprite lists
        self.items_list = arcade.SpriteList(use_spatial_hash=True)

        item = arcade.Sprite("./img/items/chest1.png", TILE_SCALING)
        item.center_x = random.randint(0, SCREEN_WIDTH)
        item.center_y = random.randint(0, SCREEN_HEIGHT)
        self.items_list.append(item)


    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        
        # Draw our sprites
        self.items_list.draw()
        
        


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
