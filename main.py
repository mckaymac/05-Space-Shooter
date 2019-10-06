import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "GUI SIMULATION"

NUM_ENEMIES = 6
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 50
KILL_SCORE = 3


class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/playerShip.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a penguin enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/spaceship.png", .25)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)            

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            #for k in self.bullet_list:
            collisions = e.collides_with_list(self.bullet_list)
            for c in collisions:
            # check for collision
                e.hp = e.hp - BULLET_DAMAGE
                c.kill()


                if(e.hp == 0):
                    e.kill()
                    self.score = self.score + KILL_SCORE

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            #fire a bullet
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    # def __init__(self, width, height, title):

    #     # Call the parent class's init function
    #     super().__init__(width, height, title)

    #     # Make the mouse disappear when it is over the window.
    #     # So we just see our object, not the pointer.
    #     self.set_mouse_visible(False)

    #     arcade.set_background_color(open_color.black)



    # def setup(self):
    #     pass 

    # def update(self, delta_time):
    #     pass

    # def on_draw(self):
    #     """ Called whenever we need to draw the window. """
    #     arcade.start_render()




    # def on_mouse_motion(self, x, y, dx, dy):
    #     """ Called to update our objects. Happens approximately 60 times per second."""
    #     pass

    # def on_mouse_press(self, x, y, button, modifiers):
    #     """
    #     Called when the user presses a mouse button.
    #     """
    #     pass

    # def on_mouse_release(self, x, y, button, modifiers):
    #     """
    #     Called when a user releases a mouse button.
    #     """
    #     pass

    # def on_key_press(self, key, modifiers):
    #     """ Called whenever the user presses a key. """
    #     if key == arcade.key.LEFT:
    #         print("Left")
    #     elif key == arcade.key.RIGHT:
    #         print("Right")
    #     elif key == arcade.key.UP:
    #         print("Up")
    #     elif key == arcade.key.DOWN:
    #         print("Down")

    # def on_key_release(self, key, modifiers):
    #     """ Called whenever a user releases a key. """
    #     pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()