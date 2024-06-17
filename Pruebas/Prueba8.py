from pyboy import PyBoy

pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', window="null", sound_emulated=True, sound=True)
pyboy.set_emulation_speed(1)

while pyboy.tick():
    pass