from utils.console import console, logger
import level, pyglet

# Init the logging
logger.select("logs")

# Creating the window
console.info(f"Creating the window")
window = pyglet.window.Window(800, 600)

# Loading the level to be displayed
batch = pyglet.graphics.Batch()
sprites = (level.get_level("level1", batch))

# Main loop
running = True
while running:
    # Drawing sequence
    window.clear()
    batch.draw()
    window.flip()

    # Handling events (very important)
    window.dispatch_events()
    # On closing of the window
    if window.has_exit or window.on_key_press(pyglet.window.key.ESCAPE, 1):
        console.info(f"Closing the window")
        running = False

window.close()