from pyboy import PyBoy
pyboy = PyBoy('ROMs/pokemon_crystal_ingles.gbc', sound=True)
with open("Pruebas/state_file.state", "rb") as f:
    pyboy.load_state(f)
while pyboy.tick():
    pass
pyboy.stop()
print("Hola")