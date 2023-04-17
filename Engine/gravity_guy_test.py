from lib import engine

class Vec2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Game:
    def __init__(self, windowWidth, windowHeight):
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.entities = [] # Entities to render

        self.player = engine.GameObject()
        self.playerRunSpeed = 8
        self.playerJumpSpeed = 12
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerJumpSpeed

        self.transform = engine.Transform()
        self.player.addTransformComponent(self.transform)
        self.transform.xPos = 100
        self.transform.yPos = 100

        self.rectangle = engine.RectangleComponent(self.transform)
        self.rectangle.setDimensions(50, 50)
        self.player.addRectangleComponent(self.rectangle)

        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/gravity-guy-test-1.lvl")
        self.tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        self.player.addTileMapComponent(self.tilemap)
        self.tileSize = self.tilemap.getSize()

        self.physics = engine.PhysicsComponent()
        self.player.addPhysicsComponent(self.physics)

        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        self.camera = engine.SideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth, 
                                                self.lvlHeight, self.rectangle)
        self.player.addCamera(self.camera)

        self.sdl.addGameObject(self.player)

        # climbing variables for climbing logic
        self.isClimbingRight = False
        self.isClimbingLeft = False
        self.curYDirection = 1 # must be 1 or -1
        self.climbingSpeed = 6
        self.fallingSpeed = 1
        

    def runLoop(self):
        inputs = self.sdl.getInput()
        while not inputs[engine.QUIT_EVENT]:
            self.update(inputs := self.sdl.getInput())
            self.render()
            self.sdl.delay(25) # Needs frame rate limiting code from test_game.cpp

    def update(self, inputs):
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
        # if inputs[engine.W_PRESSED]:
        #     pass
        # if inputs[engine.S_PRESSED]:
        #     pass
        # if inputs[engine.UP_PRESSED]:
        #     pass
        # if inputs[engine.DOWN_PRESSED]:
        #     pass
        if inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]:
            self.player.xVel = - self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingLeft:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
        elif inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
            self.player.xVel = self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingRight:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
        else:
            # set x velocity to 0
            self.player.xVel = 0
            if self.isClimbingLeft or self.isClimbingRight:
                self.player.yVel = self.curYDirection * self.fallingSpeed
        if inputs[engine.SPACE_PRESSED]:
            if self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player):
                # self.player.yVel = - self.player.yVel
                self.curYDirection *= -1
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.isClimbingRight or self.isClimbingLeft:
                if self.player.yVel > 0:
                    self.player.yVel = self.climbingSpeed
                    self.curYDirection = 1
                elif self.player.yVel < 0:
                    self.player.yVel = - self.climbingSpeed
                    self.curYDirection = -1
                else:
                    # yVel == 0, falling speed acording to curYDirection
                    self.player.yVel = self.fallingSpeed * self.curYDirection
        # update player xPos
        self.physics.UpdateX(self.player)
        collision = self.tilemap.checkCollision(self.player)
        if collision.isColliding and self.player.xVel > 0:
            # hit right wall: set xPos to correct x according to row, col
            self.transform.xPos = self.tileSize * collision.col - self.rectangle.getWidth()
            # change isClimbingRight only once
            if not self.isClimbingRight:
                self.isClimbingRight = True
                # check if on ground or ceiling
                if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
                    self.curYDirection *= -1
            self.isClimbingLeft = False
        elif collision.isColliding and self.player.xVel < 0:
            # hit left wall
            self.transform.xPos = self.tileSize * (collision.col + 1)
            # change isClimbingLeft only once
            if not self.isClimbingLeft:
                self.isClimbingLeft = True
                # check if on ground or ceiling
                if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
                    self.curYDirection *= -1
            self.isClimbingRight = False
        # check if falling off wall (pushing opposite direction than climbing wall)
        if self.isClimbingRight and not self.tilemap.isTouchingRightWall(self.player):
            self.isClimbingRight = False
            if self.player.xVel < 0:
                # player jumped off wall
                # self.curYDirection *= -1
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.player.xVel > 0:
                # player reached top of wall
                # self.curYDirection *= -1
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            else:
                # player is not pushing left or right
                self.player.yVel = 0
                self.curYDirection *= -1
        elif self.isClimbingLeft and not self.tilemap.isTouchingLeftWall(self.player):
            self.isClimbingLeft = False
            if self.player.xVel > 0:
                # player jumped off wall
                # self.curYDirection *= -1
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.player.xVel < 0:
                # player reached top of wall
                # self.curYDirection *= -1
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            else:
                # player is not pushing left or right
                self.player.yVel = 0
                self.curYDirection *= -1

        # update player yPos
        self.physics.UpdateY(self.player)
        # check if off screen
        if self.transform.yPos <= 0 or self.transform.yPos >= self.lvlHeight - self.rectangle.getHeight():
            # death: respawn
            self.transform.xPos = 100
            self.transform.yPos = 100
        collision = self.tilemap.checkCollision(self.player)
        if collision.isColliding and self.player.yVel < 0:
            # hit ceiling: set yPos to correct y according to row, col
            self.transform.yPos = self.tileSize * (collision.row + 1)
        elif collision.isColliding and self.player.yVel > 0:
            # hit floor
            self.transform.yPos = self.tileSize * (collision.row) - self.rectangle.getHeight()

        # update camera
        self.camera.Update()


    def render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        # for entity in self.entities:
        #     entity.draw(self.sdl)
        # self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        # self.rectangle.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.sdl.Render()

        self.sdl.flip()

def main():
    game = Game(960, 540)
    game.runLoop()


if __name__ == "__main__":
    main()