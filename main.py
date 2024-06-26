from pyboy import PyBoy
import sys
import sdl2
import sdl2.ext

# ------------------------ PYBOY
pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null", sound_emulated=True, sound=True)
pyboy.set_emulation_speed(1)


# ------------------------ PYSDL2
def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Pokemon Crystal Online", size=(800, 600))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    running = True
    while running:
        pyboy.tick()
        emulator_image = pyboy.screen.ndarray
        height, width, channels = emulator_image.shape
        image_bytes = emulator_image.tobytes()

        sdl_surface = sdl2.SDL_CreateRGBSurfaceFrom(image_bytes, width, height, 32,
                                                    width * 4, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)

        # Crear textura SDL2 a partir de la superficie
        texture = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, sdl_surface)
        renderer.clear()
        sdl2.SDL_RenderCopy(renderer.renderer, texture, None, None)
        renderer.present()


        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        window.refresh()
    return 0


if __name__ == "__main__":
    sys.exit(run())
