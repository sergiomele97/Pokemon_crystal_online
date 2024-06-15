import time
from pyboy import PyBoy
from sdl2 import SDL_Init, SDL_Quit, SDL_WINDOW_SHOWN, SDL_CreateWindow, SDL_CreateRenderer, SDL_RenderClear, \
    SDL_RenderCopy, SDL_RenderPresent, SDL_DestroyRenderer, SDL_DestroyWindow, SDL_WINDOWPOS_CENTERED, SDL_PollEvent, \
    SDL_QUIT, SDL_Event, SDL_WaitEvent,SDL_INIT_VIDEO,SDL_DestroyTexture
from sdl2.sdlimage import IMG_LoadTexture

# Inicializar SDL2
SDL_Init(SDL_INIT_VIDEO)

# Crear ventana SDL2
window = SDL_CreateWindow(b"PyBoy Emulator", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 160, 144, SDL_WINDOW_SHOWN)
renderer = SDL_CreateRenderer(window, -1, 0)

# Cargar el sprite (asegúrate de que la imagen esté en el mismo directorio o proporciona la ruta completa)
sprite_texture = IMG_LoadTexture(renderer, b"resources/sprite1.png")

# Cargar la ROM
rom_path = "ROMs/pokemon_crystal_ingles.gbc"
pyboy = PyBoy(rom_path, window_type="SDL2")

# Saltar la pantalla de inicio del juego, si es necesario
for _ in range(100):
    pyboy.tick()

running = True
event = SDL_Event()

while running:
    # Emulación del juego
    pyboy.tick()

    # Obtener la imagen actual del emulador
    image = pyboy.botsupport_manager().screen().screen_ndarray()

    # Convertir la imagen a una textura SDL2 (esto es un paso intermedio, no directamente necesario si ya usas SDL2 para mostrar el juego)
    # image_texture = create_texture_from_ndarray(renderer, image)  # Necesitarás implementar esto si quieres usar ndarray directamente.

    # Renderizar la pantalla del emulador
    SDL_RenderClear(renderer)
    # SDL_RenderCopy(renderer, image_texture, None, None)  # Si usas una textura SDL2 creada desde el ndarray

    # Renderizar el sprite encima de la pantalla del emulador
    SDL_RenderCopy(renderer, sprite_texture, None,
                   None)  # Cambia el rectángulo de destino si deseas posicionarlo específicamente.

    SDL_RenderPresent(renderer)

    # Manejar eventos SDL2
    while SDL_PollEvent(event) != 0:
        if event.type == SDL_QUIT:
            running = False

# Liberar recursos
SDL_DestroyTexture(sprite_texture)
# SDL_DestroyTexture(image_texture)  # Si creaste una textura desde el ndarray
SDL_DestroyRenderer(renderer)
SDL_DestroyWindow(window)
SDL_Quit()
pyboy.stop(save=False)
