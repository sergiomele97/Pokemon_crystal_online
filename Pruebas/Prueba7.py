from sdl2 import *
from pyboy import PyBoy

def main():
    # Inicializar SDL2
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
    pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null", sound_emulated=True, sound=True)
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


        # Limpiar el renderer
        SDL_RenderClear(renderer)


        # Dibujar un rectángulo personalizado
        rect = SDL_Rect(50, 50, 60, 30)
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
        SDL_RenderFillRect(renderer, rect)

        # Presentar el renderer
        SDL_RenderPresent(renderer)



    # Cerrar PyBoy
    pyboy.stop()

    # Destruir el renderer y la ventana
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)

    # Finalizar SDL2
    SDL_Quit()

if __name__ == "__main__":
    main()
