# Clase controles: Define los controles del emulador

tabla_switch = {
        '0': 'pyboy.button(\'a\')',
        '1': '001',
        '2': '010',
        '3': '011',
        '4': '100',
        '5': '101',
        '6': '110',
        '7': '111',
    }

def usa_switch(control):
    return tabla_switch.get(control)
