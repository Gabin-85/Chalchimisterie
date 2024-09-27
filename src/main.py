from utils.console import console, logger
import pyglet, level
from pyglet.gl import *

logger.select("logs")

console.info(f"Creating the window")
window = pyglet.window.Window()

images, level = level.get_level("level1")

def render():
    window.clear()
    level.draw()
    window.flip()

while True:
    render()
    window.dispatch_events()

    if window.has_exit or window.on_key_press(pyglet.window.key.ESCAPE, 1):
        break

pyglet.app.run()