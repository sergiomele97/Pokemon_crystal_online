from pyboy import PyBoy
import numpy as np
import matplotlib.pyplot as plt

# Inicializa PyBoy
pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null")
pyboy.set_emulation_speed(0)

# Asegúrate de avanzar algunos frames para que el juego inicialice correctamente
for _ in range(10):
    pyboy.tick()

# Accede a la VRAM

vram = [pyboy.memory[0xD4D8 + i] for i in range(0x1800)]  # 0x8000 to 0x97FF is typically tile data

# Convierte los datos de la VRAM en una imagen
def tile_to_image(tile_data):
    image = np.zeros((8, 8), dtype=np.uint8)
    for y in range(8):
        byte1 = tile_data[y * 2]
        byte2 = tile_data[y * 2 + 1]
        for x in range(8):
            bit1 = (byte1 >> (7 - x)) & 1
            bit2 = (byte2 >> (7 - x)) & 1
            image[y, x] = bit1 + (bit2 << 1)
    return image

# Visualiza los primeros 16 tiles como ejemplo
fig, axs = plt.subplots(2, 8, figsize=(16, 4))
for i in range(16):
    tile_data = vram[i * 16:(i + 1) * 16]
    image = tile_to_image(tile_data)
    ax = axs[i // 8, i % 8]
    ax.imshow(image, cmap='gray', interpolation='nearest')
    ax.axis('off')
plt.show()

# Cierra PyBoy
pyboy.stop()
