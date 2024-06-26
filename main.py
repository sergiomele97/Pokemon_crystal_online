from pyboy import PyBoy
from pyboy.utils import WindowEvent
import sys
import sdl2
import sdl2.ext


# ------------ GLOBAL

# ------------------------ PYBOY
pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null", sound_emulated=True, sound=True)
pyboy.set_emulation_speed(1)


# ------------------------ PYSDL2
sdl2.ext.init()
window = sdl2.ext.Window("Pokemon Crystal Online", size=(800, 600))
renderer = sdl2.ext.Renderer(window)


# ------------------------ CONTROLS
#   Check https://wiki.libsdl.org/SDL2/SDLKeycodeLookup in order to edit

KEY_DOWN = {
    sdl2.SDLK_UP: WindowEvent.PRESS_ARROW_UP,
    sdl2.SDLK_DOWN: WindowEvent.PRESS_ARROW_DOWN,
    sdl2.SDLK_RIGHT: WindowEvent.PRESS_ARROW_RIGHT,
    sdl2.SDLK_LEFT: WindowEvent.PRESS_ARROW_LEFT,
    sdl2.SDLK_a: WindowEvent.PRESS_BUTTON_A,
    sdl2.SDLK_s: WindowEvent.PRESS_BUTTON_B,
    sdl2.SDLK_RETURN: WindowEvent.PRESS_BUTTON_START,
    sdl2.SDLK_BACKSPACE: WindowEvent.PRESS_BUTTON_SELECT,
    sdl2.SDLK_SPACE: WindowEvent.PRESS_SPEED_UP,
}

KEY_UP = {
    sdl2.SDLK_UP: WindowEvent.RELEASE_ARROW_UP,
    sdl2.SDLK_DOWN: WindowEvent.RELEASE_ARROW_DOWN,
    sdl2.SDLK_RIGHT: WindowEvent.RELEASE_ARROW_RIGHT,
    sdl2.SDLK_LEFT: WindowEvent.RELEASE_ARROW_LEFT,
    sdl2.SDLK_a: WindowEvent.RELEASE_BUTTON_A,
    sdl2.SDLK_s: WindowEvent.RELEASE_BUTTON_B,
    sdl2.SDLK_RETURN: WindowEvent.RELEASE_BUTTON_START,
    sdl2.SDLK_BACKSPACE: WindowEvent.RELEASE_BUTTON_SELECT,
    sdl2.SDLK_SPACE: WindowEvent.RELEASE_SPEED_UP,
}

# ------------ RUN
def run():

    window.show()
    running = True

    while running:
        pyboy.tick()
        running = handle_events(running)
        update_background()
        window.refresh()

    return 0


def update_background():

    # 1. Gets emulator image as ndarray
    emulator_image = pyboy.screen.ndarray
    height, width, channels = emulator_image.shape
    # 2. Converts ndarray to bytes
    image_bytes = emulator_image.tobytes()
    # 3. Creates sdl surface
    sdl_surface = sdl2.SDL_CreateRGBSurfaceFrom(image_bytes, width, height, 32, width * 4, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
    # 4. Creates texture from surface
    texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, sdl_surface)
    # 5. Render
    renderer.clear()
    sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, None)
    renderer.present()


def handle_events(running):
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        elif event.type == sdl2.SDL_KEYDOWN:
            pyboy.send_input(KEY_DOWN[event.key.keysym.sym])   # pyboy-sdl2 key interface
        elif event.type == sdl2.SDL_KEYUP:
            pyboy.send_input(KEY_UP[event.key.keysym.sym])
    return running


if __name__ == "__main__":
    sys.exit(run())
