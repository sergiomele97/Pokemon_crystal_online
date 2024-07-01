# Clase Jugador: Modeliza los jugadores

class Player:

    # Global position
    x_coord = 0
    y_coord = 0

    map_bank = 0
    map_number = 0

    # Pixel position from 3 ticks before being 0 the newest    EXPLAIN
    x_coord_sprite = [0, 0, 0, 0, 0]
    y_coord_sprite = [0, 0, 0, 0, 0]

    direction = "None"


    def updateSpriteCoord(self):
        self.x_coord_sprite[3] = self.x_coord_sprite[2]
        self.x_coord_sprite[2] = self.x_coord_sprite[1]
        self.x_coord_sprite[1] = self.x_coord_sprite[0]

        self.y_coord_sprite[3] = self.y_coord_sprite[2]
        self.y_coord_sprite[2] = self.y_coord_sprite[1]
        self.y_coord_sprite[1] = self.y_coord_sprite[0]

    def isPlayerMoving(self):
        if self.x_coord_sprite[0] != self.x_coord_sprite[1] or self.y_coord_sprite[0] != self.y_coord_sprite[1]:
            self.x_coord_sprite[4] = self.x_coord_sprite[1]
            return True
        else:
            return False

    def getPlayerDirection(self):
        if self.x_coord_sprite[0] > self.x_coord_sprite[1]:
            self.direction = "left"
        if self.x_coord_sprite[0] < self.x_coord_sprite[1]:
            self.direction = "right"
        if self.y_coord_sprite[0] > self.y_coord_sprite[1]:
            self.direction = "up"
        if self.y_coord_sprite[0] < self.y_coord_sprite[1]:
            self.direction = "down"
