from pyboy import PyBoy

pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="headless", sound_emulated=True, sound=True)
pyboy.set_emulation_speed(2)

while pyboy.tick():
    pass