from sdl2 import *
from pyboy import PyBoy

def main():
    # Inicializar PySDL2
    SDL_Init(SDL_INIT_VIDEO)

    # Crear una ventana SDL2
    window = SDL_CreateWindow(b"PyBoy Custom Drawing",
                              SDL_WINDOWPOS_CENTERED,
                              SDL_WINDOWPOS_CENTERED,
                              160 * 3, 144 * 3,
                              SDL_WINDOW_SHOWN)

    # Crear un renderer para la ventana
    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)

    # Inicializar PyBoy
    pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window_type="SDL2")
    pyboy.set_emulation_speed(1)

    running = True
    event = SDL_Event()
    while running:
        while SDL_PollEvent(event):
            if event.type == SDL_QUIT:
                running = False
                break

        # Emular un frame de PyBoy
        pyboy.tick()

        # Obtener el surface de la ventana SDL2 de PyBoy
        sdl_surface = pyboy.screen.image

        # Crear una textura a partir del surface
        texture = SDL_CreateTextureFromSurface(renderer, sdl_surface)

        # Limpiar el renderer
        SDL_RenderClear(renderer)

        # Dibujar la textura de PyBoy
        SDL_RenderCopy(renderer, texture, None, None)

        # Dibujar un rectángulo personalizado
        rect = SDL_Rect(50, 50, 60, 30)
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
        SDL_RenderFillRect(renderer, rect)

        # Presentar el renderer
        SDL_RenderPresent(renderer)

        # Liberar la textura
        SDL_DestroyTexture(texture)

    # Cerrar PyBoy
    pyboy.stop()

    # Destruir el renderer y la ventana
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)

    # Finalizar SDL2
    SDL_Quit()

if __name__ == "__main__":
    main()
