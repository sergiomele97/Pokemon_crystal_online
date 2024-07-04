# Clase Jugador: Modeliza los jugadores

class Player:

    # Global position
    x_coord = 0
    y_coord = 0

    map_bank = 0
    map_number = 0

    # Pixel position from 3 ticks before being 0 the newest    EXPLAIN
    x_coord_sprite = [-1, -1, -1, -1, -1, -1]
    y_coord_sprite = [-1, -1, -1, -1, -1, -1]

    moving = "None"
    movingCycle = False
    movingCount = 0
    x_moving_correction = 0
    y_moving_correction = 0

    x_draw = 0
    y_draw = 0

    room = 0

    pixelCorrection = [0,10,10,20,20,30,30,40,40,50,50,60,60,70,70]

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
            # Correction because the emulator has a +-1 frame instability
            # An alternative would be to make pixel correction a direct function of sprite coord (many changes)
            if abs(self.x_coord_sprite[0] - self.x_coord_sprite[1]) > 3 or abs(self.y_coord_sprite[0] - self.y_coord_sprite[1]) > 3:
                self.movingCount = 1
            # End of correction
            return True
        else:
            return False

    def getPlayerDirection(self):
        # Mov horizontal
        if self.x_coord_sprite[0] != self.x_coord_sprite[1]:
            if self.x_coord_sprite[1] != 0:                         # No límite
                if self.x_coord_sprite[0] > self.x_coord_sprite[1]:
                    return "left"
                if self.x_coord_sprite[0] < self.x_coord_sprite[1]:
                    return "right"
            else:                                                   # Límite
                if self.x_coord_sprite[0] - self.x_coord_sprite[1] > 200:  # Salto a la derecha
                    return "right"
                elif self.x_coord_sprite[0] - self.x_coord_sprite[1] < 200:  # Salto a la izquierda
                    return "left"
        # Mov vertical
        if self.y_coord_sprite[0] != self.y_coord_sprite[1]:
            if self.y_coord_sprite[1] != 0:                         # No límite
                if self.y_coord_sprite[0] > self.y_coord_sprite[1]:
                    return "up"
                if self.y_coord_sprite[0] < self.y_coord_sprite[1]:
                    return "down"
            else:                                                   # Límite
                if self.y_coord_sprite[0] - self.y_coord_sprite[1] > 200:  # Salto abajo
                    return "down"
                elif self.y_coord_sprite[0] - self.y_coord_sprite[1] < 200:  # Salto arriba
                    return "up"


    def updateMovingCorrection(self):
        if self.moving == "left":
            self.x_moving_correction = self.pixelCorrection[self.movingCount]
        elif self.moving == "right":
            self.x_moving_correction = - self.pixelCorrection[self.movingCount]
        elif self.moving == "up":
            self.y_moving_correction = self.pixelCorrection[self.movingCount]
        elif self.moving == "down":
            self.y_moving_correction = - self.pixelCorrection[self.movingCount]

    def endOfMovingCycle(self):
        self.movingCycle = False
        self.movingCount = 0
        self.x_moving_correction = 0
        self.y_moving_correction = 0
        print("Moving cycle OFF-----------------------------")