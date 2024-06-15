from pyboy import PyBoy

# Inicializa PyBoy
pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null")
pyboy.set_emulation_speed(0)

# Asegúrate de avanzar algunos frames para que el juego inicialice correctamente
for _ in range(10):
    pyboy.tick()

# Obtén acceso a la VRAM
vram = pyboy.memory[0x8000]

# Define los datos del sprite (ejemplo simple, 8x8 pixels, 2 bits por pixel)
# Esto debe ser ajustado para que coincida con el formato de los sprites de Game Boy
sprite_data = [
    0b00000001
]

# Carga el sprite en la VRAM (por ejemplo, en la dirección 0x8000)
'''
for i, byte in enumerate(sprite_data):
    pyboy.memory[0x8000 + i] = byte


# Configura los atributos del sprite
sprite_index = 0  # Índice del sprite en la tabla de sprites
x_position = 50  # Posición X en la pantalla
y_position = 50  # Posición Y en la pantalla

# Escribe los atributos del sprite en la OAM (Object Attribute Memory)
pyboy.memory[0xFE00 + sprite_index * 4] = y_position        # Y Position
pyboy.memory[0xFE00 + sprite_index * 4 + 1] = x_position     # X Position
pyboy.memory[0xFE00 + sprite_index * 4 + 2] = 0         # Tile Index (0 para el primer sprite en VRAM)
pyboy.memory[0xFE00 + sprite_index * 4 + 3] = 0         # Atributos (sin flip, prioridad, etc.)
'''
# Avanza algunos frames para que los cambios se reflejen
for _ in range(10):

    pyboy.tick()

# Guarda el estado del emulador para revisar el resultado
with open("state_file.state", "rb") as f:
    pyboy.load_state(f)


######################### emular


pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', sound=True)


while pyboy.tick():
    '''
    for i in range(200):
        pyboy.memory[0xC4A0 + i] = i
    '''


    pyboy.memory[0xFE10] = 40
    pyboy.memory[0xFE11] = 40
    pyboy.memory[0xFE12] = pyboy.memory[0xFE02]
    pyboy.memory[0xFE13] = pyboy.memory[0xFE03]



    pass


for i in range(40):
    print(pyboy.get_sprite(i))

print(pyboy.get_sprite_by_tile_identifier([3]))

with open("state_file.state", "wb") as f:
    pyboy.save_state(f)
pyboy.stop()
