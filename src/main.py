from utils.console import console, logger
import pyglet, level

logger.select("logs")

console.info(f"Creating the window")
window = pyglet.window.Window()

level = level.get_level("level1")

@window.event
def on_draw():
    window.clear()
    for image in level:
        image.blit(0, 0, 0, 960, 640)

pyglet.app.run()