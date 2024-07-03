# Clase Jugador: Modeliza los jugadores

class Player:

    # Global position
    x_coord = 0
    y_coord = 0

    map_bank = 0
    map_number = 0

    # Pixel position from 3 ticks before being 0 the newest    EXPLAIN
    x_coord_sprite = [-1, -1, -1, -1, -1, -1]
    y_coord_sprite = [-1, -1, -1, -1, -1 - 1]

    direction = "None"
    movingCycle = False
    movingCount = 0
    x_moving_correction = 0

    pixelCorrection = [10,10,20,20,30,30,40,40,50,50,60,60,-10,-10,0,0]

    def updateSpriteCoord(self):
        self.x_coord_sprite[4] = self.x_coord_sprite[3]
        self.x_coord_sprite[3] = self.x_coord_sprite[2]
        self.x_coord_sprite[2] = self.x_coord_sprite[1]
        self.x_coord_sprite[1] = self.x_coord_sprite[0]

        self.y_coord_sprite[4] = self.y_coord_sprite[3]
        self.y_coord_sprite[3] = self.y_coord_sprite[2]
        self.y_coord_sprite[2] = self.y_coord_sprite[1]
        self.y_coord_sprite[1] = self.y_coord_sprite[0]

    def isPlayerMoving(self):
        if self.x_coord_sprite[0] != self.x_coord_sprite[1] or self.y_coord_sprite[0] != self.y_coord_sprite[1]:
            return True
        else:
            return False

    def getPlayerDirection(self):
        if self.x_coord_sprite[0] > self.x_coord_sprite[1]:
            return "left"
        if self.x_coord_sprite[0] < self.x_coord_sprite[1]:
            return "right"
        if self.y_coord_sprite[0] > self.y_coord_sprite[1]:
            return "up"
        if self.y_coord_sprite[0] < self.y_coord_sprite[1]:
            return "down"

    def updateMovingCorrection(self):
        if self.direction == "left":
            self.x_moving_correction = self.pixelCorrection[self.movingCount]
        if self.direction == "right":
            self.x_moving_correction = - self.pixelCorrection[self.movingCount]

    def endOfMovingCycle(self):
        self.x_coord_sprite[5] = self.x_coord_sprite[0]
        self.movingCycle = False