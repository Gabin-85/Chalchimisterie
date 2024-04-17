# This a simple file (actually but after no) who is in charge of using the map.

def get_map_zoom(zoom, screen_width, screen_height):
    # Get the real zoom
        if screen_width < screen_height:
            map_zoom = screen_height/800*zoom
        else:
            map_zoom = screen_width/800*zoom
        return map_zoom

