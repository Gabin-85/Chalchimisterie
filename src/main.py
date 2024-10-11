from utils.console import logger
from ui import SpriteRect
import pyglet, level, cProfile

# Init the logging
logger.select("logs")

# Creating the window
window = pyglet.window.Window(800, 600, "Chalchimisterie", True)

level1 = SpriteRect()
level1.add_sprite(level.get_level("level1"))

@window.event
def on_draw():

    level1.set_size(window.width, window.height)

    window.clear()
    level1.draw()

@window.event
def on_key_press(symbol, modifiers):

    if symbol == pyglet.window.key.ESCAPE:
        window.close()

pyglet.app.run()