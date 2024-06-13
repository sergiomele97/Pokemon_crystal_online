from pyboy import PyBoy
pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', sound=True)
while pyboy.tick():
    pass
pyboy.stop()
