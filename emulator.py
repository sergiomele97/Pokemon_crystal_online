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
    player2.map_number = 5
    player2.x_coord = 4
    player2.y_coord = 9

    player3 = Player()
    player3.map_bank = 24
    player3.map_number = 4
    player3.x_coord = 4
    player3.y_coord = 6

    current_map_bank = 0
    current_map_number = 0
    current_x = 0
    current_y = 0

    collision_down = 0
    collision_up = 0
    collision_left = 0
    collision_right = 0

    sprite_coord_changes = "Still"
    observing_changes = True
    draw_allowed = True

    transition_type = "door"
    transition_times = {
        "door_start": 20,
        "door_end": 38,
        "red_door_start": 0,
        "red_door_end": 15,
    }

    def __init__(self):
        print("Constructor")

    # ------------ RUN
    def run(self):

        self.window.show()
        self.open_state()
        running = True
        self.get_ram_data()
        self.update_coords()

        while running:
            self.get_ram_data()    # Coords from last tick
            self.pyboy.tick()
            running = self.handle_events(running)
            self.update_screen()
            self.window.refresh()

    def update_screen(self):
        self.renderer.clear()        # 1. Clear
        self.update_background()     # 2. Update background
        self.update_sprites()        # 3. Update sprites
        self.renderer.present()      # 4. Present

    def update_sprites(self):
        # Load the sprite (assuming you have a transparent BMP)
        sprite_factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
        sprite = sprite_factory.from_image("Resources/mainOW.bmp")

        print("")
        print(self.player.x_coord_sprite)
        print(self.player.y_coord_sprite)

        self.update_local_context()  # Qué cambios ha habido en xy sprite coords

        # 1. Ciclos

        if self.player.movingCycle:
            self.continueMovingCycle()
        if self.player.transitionCycle:
            self.continueTransitionCycle()

        # 2. Triggers de ciclo
        if self.is_red_door_transition():
            self.start_transition_cycle()

        if self.observing_changes:
            # Hierarchy: transition > event > moving .

            if self.sprite_coord_changes == "None":
                pass

            elif self.is_event():
                print("event")
                pass

            elif self.is_movement():
                self.start_movement_cycle()
                self.continueMovingCycle()      # 1 Iteration

        # 3. Dibujar players
        self.draw_player(sprite)


    '''
        This function must define what is going on in the emulator (Player either: moving, event or changing the map
        Its parameters are: x_coord_sprite, y_coord_sprite.
        
        - Things that might trigger a stop in drawing: 
            - Map transistion cycle: f(collision info + moving cycle)
                - Map transition cycle is the only thing that might change the self. map and map number variables.
        - it might work as a hierarchy: transition cycle > event > moving cycle.
            - transition cycle cancels the possibility of event.
        
    '''
    def update_local_context(self):
        if self.player.x_coord_sprite[0] == self.player.x_coord_sprite[1] and self.player.y_coord_sprite[0] == self.player.y_coord_sprite[1]:
            self.sprite_coord_changes = "None"    # No changes
        if self.player.x_coord_sprite[0] != self.player.x_coord_sprite[1] and self.player.y_coord_sprite[0] != self.player.y_coord_sprite[1]:
            self.sprite_coord_changes = "Both"    # Change in both
        if self.player.x_coord_sprite[0] != self.player.x_coord_sprite[1] and self.player.y_coord_sprite[0] == self.player.y_coord_sprite[1]:
            self.sprite_coord_changes = "x"  # Change in x
        if self.player.x_coord_sprite[0] == self.player.x_coord_sprite[1] and self.player.y_coord_sprite[0] != self.player.y_coord_sprite[1]:
            self.sprite_coord_changes = "y"  # Change in y

    # TRANSITION CYCLE ------------------------------------------------------------------------------------------

    def continueTransitionCycle(self):
        if self.player.transitionCount > 40:    # Potenciales bugs se pueden solucionar modificando esta variable
            self.end_transition_cycle()
            return 0
        self.player.transitionCount = self.player.transitionCount + 1
        # Se ejecute solo cuando haya terminado el moving cycle:
        if not self.player.movingCycle:
            self.update_coords()

        if self.transition_type == "door":
            if self.transition_times["door_start"] < self.player.transitionCount < self.transition_times["door_end"]:
                self.draw_allowed = False
            else:
                self.draw_allowed = True
        if self.transition_type == "red_door":
            if self.transition_times["red_door_start"] < self.player.transitionCount < self.transition_times["red_door_end"]:
                self.draw_allowed = False
            else:
                self.draw_allowed = True

    def end_transition_cycle(self):
        self.player.transitionCycle = False
        self.draw_allowed = True
        print("Transition cycle OFF-----------------------------------")

    def start_transition_cycle(self):
        self.player.transitionCycle = True
        self.player.transitionCount = 0
        print("Transition cycle ON-----------------------------------")

    def is_transition(self):
        # 113 transition aka door transition
        if self.player.moving == "down" and self.collision_down == 113:
            self.transition_type = "door"
            return True
        if self.player.moving == "up" and self.collision_up == 113:
            self.transition_type = "door"
            return True
        if self.player.moving == "left" and self.collision_left == 113:
            self.transition_type = "door"
            return True
        if self.player.moving == "right" and self.collision_right == 113:
            self.transition_type = "door"
            return True
        return False

    def is_red_door_transition(self):
        # 255 transition aka red transition
        if self.player.y_coord_sprite[0] == self.player.y_coord_sprite[1] == self.player.y_coord_sprite[2] == self.player.y_coord_sprite[3] == 223:
            print("red door transition")
            self.transition_type = "red_door"
            return True
        return False

    # ---------------------------------------------------------------------------------------------------------
    # MOVEMENT CYCLE ------------------------------------------------------------------------------------------
    def is_movement(self):
        if self.player.x_coord_sprite[0] != self.player.x_coord_sprite[1] or self.player.y_coord_sprite[0] != self.player.y_coord_sprite[1]:
            # Correction because the emulator has a +-1 frame instability
            # An alternative would be to make pixel correction a direct function of sprite coord (many changes)
            if abs(self.player.x_coord_sprite[0] - self.player.x_coord_sprite[1]) == 4 or abs(self.player.y_coord_sprite[0] - self.player.y_coord_sprite[1]) == 4:
                self.player.movingCount = 1
            if abs(self.player.x_coord_sprite[0] - self.player.x_coord_sprite[1]) == 252 or abs(self.player.y_coord_sprite[0] - self.player.y_coord_sprite[1]) == 252:
                self.player.movingCount = 1
            # End of correction
            return True
        else:
            return False

    def start_movement_cycle(self):
        self.update_coords()
        self.observing_changes = False
        self.player.movingCycle = True
        self.player.moving = self.player.getPlayerDirection()
        self.player.x_coord_sprite[5] = self.player.x_coord_sprite[1]
        self.player.y_coord_sprite[5] = self.player.y_coord_sprite[1]
        print("Moving cycle ON-----------------------------------")
        print(self.player.moving)

        if self.is_transition():
            self.start_transition_cycle()
            pass

    def continueMovingCycle(self):
        # End cycle
        if self.player.movingCount > 14:
            self.endOfMovingCycle()
        # In moving cycle event
        elif self.is_event():
            self.in_movement_event()
            pass
        # Continue cycle
        else:
            if abs(self.player.y_coord_sprite[0] - self.player.y_coord_sprite[2]) == 4 and self.player.y_coord_sprite[2] != self.player.y_coord_sprite[5]:
                self.player.movingCount = self.player.movingCount + 1
                print("SALTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            self.player.updateMovingCorrection()
            self.player.movingCount = self.player.movingCount + 1

    def endOfMovingCycle(self):
        self.observing_changes = True
        self.player.movingCycle = False
        self.player.movingCount = 0
        self.player.moving = "None"
        self.player.x_moving_correction = 0
        self.player.y_moving_correction = 0
        self.update_coords()

        print("Moving cycle OFF-----------------------------")

    # ---------------------------------------------------------------------------------------------------------
    def in_movement_event(self):    # Al cambiar de zona deja de actualizar durante 1 frame
        self.player.x_coord_sprite[0] = self.player.x_coord_sprite[1]
        self.player.y_coord_sprite[0] = self.player.y_coord_sprite[1]

    def is_event(self):
        if self.sprite_coord_changes == "Both":
            return True
        if self.sprite_coord_changes == "x":
            if 4 < abs(self.player.x_coord_sprite[0] - self.player.x_coord_sprite[1]) < 251:
                return True
        if self.sprite_coord_changes == "y":
            if 4 < abs(self.player.y_coord_sprite[0] - self.player.y_coord_sprite[1]) < 251:
                return True
        return False

    def draw_player(self, sprite):
        if not self.draw_allowed:
            return 0

        if self.current_map_bank == self.player2.map_bank and self.current_map_number == self.player2.map_number:

            #   x_draw = (x jugador2 - x jugador1 + cuadrados hasta centro pantalla) * pixeles/cuadrado
            self.player2.x_draw = (self.player2.x_coord - self.current_x + 4) * 80 + self.player.x_moving_correction
            self.player2.y_draw = (self.player2.y_coord - self.current_y + 4) * 80 - 20 + self.player.y_moving_correction

            print(self.player2.x_draw)
            print(self.player2.y_draw)
            print("")
            # Copy to render
            self.renderer.copy(sprite, srcrect=(17, 0, 16, 16), dstrect=(self.player2.x_draw, self.player2.y_draw, 80, 80))  # Sprite y rectangulo animacion

        if self.current_map_bank == self.player3.map_bank and self.current_map_number == self.player3.map_number:

            self.player3.x_draw = (self.player3.x_coord - self.current_x + 4) * 80 + self.player.x_moving_correction
            self.player3.y_draw = (self.player3.y_coord - self.current_y + 4) * 80 - 20 + self.player.y_moving_correction

            self.renderer.copy(sprite, srcrect=(17, 0, 16, 16), dstrect=(self.player3.x_draw, self.player3.y_draw, 80, 80))

    def update_coords(self):
        self.current_map_bank = self.player.map_bank
        self.current_map_number = self.player.map_number
        self.current_x = self.player.x_coord
        self.current_y = self.player.y_coord
        print("update")

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

    def get_ram_data(self):
        self.player.x_coord = self.pyboy.memory[0xDCB8]
        self.player.y_coord = self.pyboy.memory[0xDCB7]

        self.player.map_number = self.pyboy.memory[0xDCB6]
        self.player.map_bank = self.pyboy.memory[0xDCB5]
        print("map and bank")
        print(self.player.map_number)
        print(self.player.map_bank)
        print(self.current_map_number)
        print(self.current_map_bank)

        self.player.updateSpriteCoord()
        self.player.x_coord_sprite[0] = self.pyboy.memory[0xD14C]
        self.player.y_coord_sprite[0] = self.pyboy.memory[0xD14D]

        self.collision_down = self.pyboy.memory[0xC2FA]
        self.collision_up = self.pyboy.memory[0xC2FB]
        self.collision_left = self.pyboy.memory[0xC2FC]
        self.collision_right = self.pyboy.memory[0xC2FD]

        print(self.collision_down)
        print(self.collision_up)
        print(self.collision_left)
        print(self.collision_right)


        # Mi siguiente idea es tratar de clasificar los eventos con la info que
        # repiten en x e y sprite coords: EJ parece que al pasar por una puerta
        # roja: siempre hay 3 y sprite coords = 223


