import pygame

allowed = [pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]
def set_allowed_event(events:list[pygame.event.Event]):
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(events)

class state:
    running = True
    key:set[int] = set()
    key_press:set[int] = set()
    key_unpress:set[int] = set()

def quit_game() -> None:
    state.running = False

def key_press(event:dict) -> None:
    state.key.add(event["key"])
    state.key_press.add(event["key"])

def key_unpress(event:dict) -> None:
    state.key.discard(event["key"])
    state.key_unpress.add(event["key"])

def key_clear() -> None:
    state.key_press.clear()
    state.key_unpress.clear()

def update():
    key_clear()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                quit_game()
            case pygame.KEYDOWN:
                key_press(event.dict)
            case pygame.KEYUP:
                key_unpress(event.dict)
            case _:
                pass