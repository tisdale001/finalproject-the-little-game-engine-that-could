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
        self.transform.setPosition(100, 100)

        self.maxFrameDict = {}
        '''
        CREATE A SPRITE
        Spritesheets should be located in the Assets folder. Use the "loadImage"
        function to import one.
        "setRectangleDimensions" sets the size of the sprite on the screen.
        
        "setSpriteSheetDimensions" is for correctly iterating through the spritesheet.
        (width of sprite, height of sprite, max num sprites in a row, total num sprites, numPixelsToTrimFromWidth)
        numPixelsToTrimFromWidth : this parameter tells how many pixels are to be taken off each sprite image, in case
        there is extra space between images.
        '''
        self.run_right_sprite = engine.Sprite(self.transform, True)
        self.run_right_sprite.setRectangleDimensions(32, 48)
        self.run_right_sprite.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_right_sprite.loadImage("Assets/spritesheets/Cyborg_run_right.bmp", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.run_right_sprite)
        self.maxFrameDict[str(self.run_right_sprite)] = 6

        self.run_left_sprite = engine.Sprite(self.transform, False)
        self.run_left_sprite.setRectangleDimensions(32, 48)
        self.run_left_sprite.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_left_sprite.loadImage("Assets/spritesheets/Cyborg_run_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_sprite)] = 6

        self.run_right_on_ceiling = engine.Sprite(self.transform, True)
        self.run_right_on_ceiling.setRectangleDimensions(32, 48)
        self.run_right_on_ceiling.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_right_on_ceiling.loadImage("Assets/spritesheets/Cyborg_run_ceiling_and_right.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_right_on_ceiling)] = 6

        self.run_left_on_ceiling = engine.Sprite(self.transform, False)
        self.run_left_on_ceiling.setRectangleDimensions(32, 48)
        self.run_left_on_ceiling.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_left_on_ceiling.loadImage("Assets/spritesheets/Cyborg_run_ceiling_and_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_on_ceiling)] = 6

        self.idle_right = engine.Sprite(self.transform, True)
        self.idle_right.setRectangleDimensions(26, 48)
        self.idle_right.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_right.loadImage("Assets/spritesheets/Cyborg_idle_right.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right)] = 4

        self.idle_left = engine.Sprite(self.transform, False)
        self.idle_left.setRectangleDimensions(26, 48)
        self.idle_left.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_left.loadImage("Assets/spritesheets/Cyborg_idle_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left)] = 4

        self.idle_right_on_ceiling = engine.Sprite(self.transform, True)
        self.idle_right_on_ceiling.setRectangleDimensions(26, 48)
        self.idle_right_on_ceiling.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_right_on_ceiling.loadImage("Assets/spritesheets/Cyborg_idle_right_on_ceiling.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right_on_ceiling)] = 4

        self.idle_left_on_ceiling = engine.Sprite(self.transform, False)
        self.idle_left_on_ceiling.setRectangleDimensions(26, 48)
        self.idle_left_on_ceiling.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_left_on_ceiling.loadImage("Assets/spritesheets/Cyborg_idle_left_on_ceiling.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left_on_ceiling)] = 4

        self.climb_up = engine.Sprite(self.transform, True)
        self.climb_up.setRectangleDimensions(26, 48)
        self.climb_up.setSpriteSheetDimensions(48, 48, 6, 6, 24)
        self.climb_up.loadImage("Assets/spritesheets/Cyborg_climb.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.climb_up)] = 6

        self.climb_down = engine.Sprite(self.transform, True)
        self.climb_down.setRectangleDimensions(26, 48)
        self.climb_down.setSpriteSheetDimensions(48, 48, 6, 6, 24)
        self.climb_down.loadImage("Assets/spritesheets/Cyborg_climb_down.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.climb_down)] = 6

        # self.rectangle = engine.RectangleComponent(self.transform)
        # self.rectangle.setDimensions(50, 50)
        # self.player.addRectangleComponent(self.rectangle)

        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/gravity-guy-test-1.lvl")
        self.tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        self.player.addTileMapComponent(self.tilemap)
        self.tileSize = self.tilemap.getSize()

        self.physics = engine.PhysicsComponent()
        self.player.addPhysicsComponent(self.physics)

        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        self.camera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth, 
                                                self.lvlHeight, self.player.mSprite)

        self.cameraOffsetX = 0
        self.cameraOffsetY = 0

        '''
        Need to keep track of number of frames in the sprite sheet. 
        '''
        self.currentFrame = 0
        self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]

        # climbing variables for climbing logic
        self.isClimbingRight = False
        self.isClimbingLeft = False
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
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
            self.curXDirection = -1
            self.player.xVel = - self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingLeft:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
                if self.curYDirection > 0:
                    # gravity is down, change to climb_up sprite
                    self.player.addSpriteComponent(self.climb_up)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_up)]
                else:
                    # gravity is up, change to climb_down sprite
                    self.player.addSpriteComponent(self.climb_down)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_down)]
            else:
                if self.curYDirection > 0:
                    # change to running left
                    self.player.addSpriteComponent(self.run_left_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_left_sprite)]
                else:
                    # change to running left on ceiling
                    self.player.addSpriteComponent(self.run_left_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_left_on_ceiling)]
        elif inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
            self.curXDirection = 1
            self.player.xVel = self.playerRunSpeed
            self.player.yVel = self.playerJumpSpeed * self.curYDirection
            if self.isClimbingRight:
                self.player.yVel = self.climbingSpeed * (- self.curYDirection)
                if self.curYDirection > 0:
                    # gravity is down, change to climb_up sprite
                    self.player.addSpriteComponent(self.climb_up)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_up)]
                else:
                    # gravity is up, change to climb_down sprite
                    self.player.addSpriteComponent(self.climb_down)
                    self.currentMaxFrame = self.maxFrameDict[str(self.climb_down)]
            else:
                if self.curYDirection > 0:
                    # change to running right
                    self.player.addSpriteComponent(self.run_right_sprite)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]
                else:
                    # change to running right on ceiling
                    self.player.addSpriteComponent(self.run_right_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.run_right_on_ceiling)]
        else:
            # set x velocity to 0
            self.player.xVel = 0
            # change to idle sprite based on self.curXDirection and self.curYDirection
            if self.curYDirection > 0:
                if self.curXDirection > 0:
                    # switch to idle_right
                    self.player.addSpriteComponent(self.idle_right)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_right)]
                else:
                    # switch to idle_left
                    self.player.addSpriteComponent(self.idle_left)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_left)]
            else:
                if self.curXDirection > 0:
                    # switch to idle_right_on_ceiling
                    self.player.addSpriteComponent(self.idle_right_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_right_on_ceiling)]
                else:
                    # switch to idle_left_on_ceiling
                    self.player.addSpriteComponent(self.idle_left_on_ceiling)
                    self.currentMaxFrame = self.maxFrameDict[str(self.idle_left_on_ceiling)]

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
            self.transform.xPos = self.tileSize * collision.col - self.player.mSprite.getWidth()
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
        if self.transform.yPos <= 0 or self.transform.yPos >= self.lvlHeight - self.player.mSprite.getHeight():
            # death: respawn
            self.transform.xPos = 100
            self.transform.yPos = 100
        collision = self.tilemap.checkCollision(self.player)
        if collision.isColliding and self.player.yVel < 0:
            # hit ceiling: set yPos to correct y according to row, col
            self.transform.yPos = self.tileSize * (collision.row + 1)
        elif collision.isColliding and self.player.yVel > 0:
            # hit floor
            self.transform.yPos = self.tileSize * (collision.row) - self.player.mSprite.getHeight()

        # update frame
        if self.currentFrame >= self.currentMaxFrame:
            self.currentFrame = 0
        else:
            self.currentFrame += 1
        self.player.mSprite.update(0, 0, self.currentFrame)

        # update camera
        self.camera.Update()


    def render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        # for entity in self.entities:
        #     entity.draw(self.sdl)
        self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.player.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.sdl.flip()

    

def main():
    game = Game(960, 540)
    game.runLoop()


if __name__ == "__main__":
    main()