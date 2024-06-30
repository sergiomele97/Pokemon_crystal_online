from pyboy import PyBoy
from pyboy.utils import WindowEvent
from player import Player
import sdl2
import sdl2.ext



class Emulator:

    # ------------------------ PYBOY
    pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null", sound_emulated=True, sound=True)
    pyboy.set_emulation_speed(1)

    # ------------------------ PYSDL2
    sdl2.ext.init()
    window = sdl2.ext.Window("Pokemon Crystal Online", size=(800, 720))
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

    # ------------------------ PLAYER
    player = Player()

    player2 = Player()
    player2.map_bank = 24
    player2.map_number = 4
    player2.x_coord = 9
    player2.y_coord = 7



    def __init__(self):
        print("Constructor")

    # ------------ RUN
    def run(self):

        self.window.show()
        self.open_state()
        running = True

        while running:
            self.pyboy.tick()
            self.get_player_coords()
            running = self.handle_events(running)
            self.update_screen()
            self.window.refresh()

    def update_screen(self):
        self.renderer.clear()        # 1. Clear
        self.update_background()     # 2. Update background
        self.update_sprites()        # 3. Update sprites
        self.renderer.present()      # 4. Present

    def update_sprites(self):
        # 1. Load the sprite (assuming you have a transparent BMP)
        sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
        sprite = sprite_factory.from_image("Resources/mainOW.bmp")

        ########################### DEBUG

        # Corrección: para actualizar el sprite con precisión de pixel y no de cuadrado



        #   x_draw = (x jugador2 - x jugador1 + cuadrados hasta centro pantalla) * pixeles/cuadrado

        x_draw = (self.player2.x_coord - self.player.x_coord + 4) * 80
        y_draw = (self.player2.y_coord - self.player.y_coord + 4) * 80 - 20

        # 2. Render
        self.renderer.copy(sprite, srcrect=(17, 0, 16, 16), dstrect=(x_draw, y_draw, 80, 80))  # Sprite y rectangulo animacion

        ########################### DEBUG

    def update_background(self):
        # 1. Gets emulator image as ndarray
        emulator_image = self.pyboy.screen.ndarray
        height, width, channels = emulator_image.shape
        # 2. Converts ndarray to bytes
        image_bytes = emulator_image.tobytes()
        # 3. Creates sdl surface
        sdl_surface = sdl2.SDL_CreateRGBSurfaceFrom(image_bytes, width, height, 32, width * 4, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)
        # 4. Creates texture from surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.renderer.sdlrenderer, sdl_surface)
        # 5. Render
        sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, texture, None, None)  # Fondo

    def handle_events(self, running):
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                self.save_state()          # Guarda estado emulador
                running = False
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                input_value = self.KEY_DOWN.get(event.key.keysym.sym, None)   # pyboy-sdl2 key interface
                if input_value:
                    self.pyboy.send_input(input_value)
            elif event.type == sdl2.SDL_KEYUP:
                input_value = self.KEY_UP.get(event.key.keysym.sym, None)
                if input_value:
                    self.pyboy.send_input(input_value)

        return running

    def open_state(self):
        # Load file
        with open("States/state_file.state", "rb") as f:
            self.pyboy.load_state(f)

    def save_state(self):
        # Save to file
        with open("States/state_file.state", "wb") as f:
            self.pyboy.save_state(f)

    def get_player_coords(self):
        self.player.x_coord = self.pyboy.memory[0xDCB8]
        self.player.y_coord = self.pyboy.memory[0xDCB7]
        self.player.x_coord_sprite = self.pyboy.memory[0xD14C]
        self.player.y_coord_sprite = self.pyboy.memory[0xD14D]
        self.player.map_number = self.pyboy.memory[0xDCB6]
        self.player.map_bank = self.pyboy.memory[0xDCB5]

        print("")
        print("sprite X = ", self.pyboy.memory[0xD14C])    # sprite X
        print("sprite Y = ", self.pyboy.memory[0xD14D])    # sprite Y
        print("player X = ", self.player.x_coord)
        print("player Y = ", self.player.y_coord)
        print("map bank = ", self.pyboy.memory[0xDCB5])
        print("map number = ", self.pyboy.memory[0xDCB6])



