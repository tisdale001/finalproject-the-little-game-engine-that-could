from lib import engine


# Represents a Gravity Guy Game
class Game:
    # Initialize Game
    def __init__(self, windowWidth, windowHeight):
        # SDL Setup
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        # Tilemap Setup
        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/gravity-guy-test-2.lvl")
        self.tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        self.tileSize = self.tilemap.getSize()
        # Level size
        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize
        # Physics Setup
        self.physics = engine.PhysicsComponent()
        # Entities to render
        self.entities = [] 

        # Player Object Setup
        self.player = engine.GameObject()
        # Player Transform Component
        self.playerTransform = engine.Transform()
        self.player.addTransformComponent(self.playerTransform)
        self.playerTransform.xPos = 100
        self.playerTransform.yPos = 100

        # # Player Rectangle Component
        # self.playerRectangle = engine.RectangleComponent(self.playerTransform)
        # self.playerRectangle.setDimensions(50, 50)
        # self.playerRectangle.setColor(150, 255, 255, 255)
        # self.player.addRectangleComponent(self.playerRectangle)

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
        self.run_right_sprite = engine.Sprite(self.playerTransform, True)
        self.run_right_sprite.setRectangleDimensions(32, 48)
        self.run_right_sprite.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_right_sprite.loadImage("Assets/spritesheets/Cyborg_run_right.bmp", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.run_right_sprite)
        self.maxFrameDict[str(self.run_right_sprite)] = 6

        self.run_left_sprite = engine.Sprite(self.playerTransform, False)
        self.run_left_sprite.setRectangleDimensions(32, 48)
        self.run_left_sprite.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_left_sprite.loadImage("Assets/spritesheets/Cyborg_run_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_sprite)] = 6

        self.run_right_on_ceiling = engine.Sprite(self.playerTransform, True)
        self.run_right_on_ceiling.setRectangleDimensions(32, 48)
        self.run_right_on_ceiling.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_right_on_ceiling.loadImage("Assets/spritesheets/Cyborg_run_ceiling_and_right.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_right_on_ceiling)] = 6

        self.run_left_on_ceiling = engine.Sprite(self.playerTransform, False)
        self.run_left_on_ceiling.setRectangleDimensions(32, 48)
        self.run_left_on_ceiling.setSpriteSheetDimensions(48, 48, 6, 6, 16)
        self.run_left_on_ceiling.loadImage("Assets/spritesheets/Cyborg_run_ceiling_and_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.run_left_on_ceiling)] = 6

        self.idle_right = engine.Sprite(self.playerTransform, True)
        self.idle_right.setRectangleDimensions(26, 48)
        self.idle_right.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_right.loadImage("Assets/spritesheets/Cyborg_idle_right.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right)] = 4

        self.idle_left = engine.Sprite(self.playerTransform, False)
        self.idle_left.setRectangleDimensions(26, 48)
        self.idle_left.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_left.loadImage("Assets/spritesheets/Cyborg_idle_left.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left)] = 4

        self.idle_right_on_ceiling = engine.Sprite(self.playerTransform, True)
        self.idle_right_on_ceiling.setRectangleDimensions(26, 48)
        self.idle_right_on_ceiling.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_right_on_ceiling.loadImage("Assets/spritesheets/Cyborg_idle_right_on_ceiling.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_right_on_ceiling)] = 4

        self.idle_left_on_ceiling = engine.Sprite(self.playerTransform, False)
        self.idle_left_on_ceiling.setRectangleDimensions(26, 48)
        self.idle_left_on_ceiling.setSpriteSheetDimensions(48, 48, 4, 4, 24)
        self.idle_left_on_ceiling.loadImage("Assets/spritesheets/Cyborg_idle_left_on_ceiling.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.idle_left_on_ceiling)] = 4

        self.climb_up = engine.Sprite(self.playerTransform, True)
        self.climb_up.setRectangleDimensions(26, 48)
        self.climb_up.setSpriteSheetDimensions(48, 48, 6, 6, 24)
        self.climb_up.loadImage("Assets/spritesheets/Cyborg_climb.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.climb_up)] = 6

        self.climb_down = engine.Sprite(self.playerTransform, True)
        self.climb_down.setRectangleDimensions(26, 48)
        self.climb_down.setSpriteSheetDimensions(48, 48, 6, 6, 24)
        self.climb_down.loadImage("Assets/spritesheets/Cyborg_climb_down.bmp", self.sdl.getSDLRenderer())
        self.maxFrameDict[str(self.climb_down)] = 6

        # Player Tilemap Component
        self.player.addTileMapComponent(self.tilemap)
        # Player Physics Component
        self.player.addPhysicsComponent(self.physics)

        # Camera Setup
        self.camera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth, 
                                                self.lvlHeight, self.player.mSprite)
        self.cameraOffsetX = 0
        self.cameraOffsetY = 0

        '''
        Need to keep track of number of frames in the sprite sheet. 
        '''
        self.currentFrame = 0
        self.currentMaxFrame = self.maxFrameDict[str(self.run_right_sprite)]

        # Climbing variables
        self.isClimbingRight = False
        self.isClimbingLeft = False
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
        self.climbingSpeed = 6
        self.fallingSpeed = 1

        # Sounds
        self.music = engine.Music()
        self.music.SetMusic("Assets/Sounds/SteamtechMayhem.wav")
        self.gameOverSound = engine.Sound()
        self.gameOverSound.SetSound("Assets/Sounds/GameOver.wav")
        self.winSound = engine.Sound()
        self.winSound.SetSound("Assets/Sounds/Win.wav")
        self.jumpSound = engine.Sound()
        self.jumpSound.SetSound("Assets/Sounds/Jump.wav")
        self.speedUpSound = engine.Sound()
        self.speedUpSound.SetSound("Assets/Sounds/SpeedUp.wav")

        # Gravity Guy Settings
        self.playerRunSpeed = 8
        self.playerJumpSpeed = 12
        self.autoRun = False
        self.spaceTapErrorLenience = 0.1
        # Game Variables
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerJumpSpeed
        self.timeSinceSpaceTapped = 99
        self.alreadySpedUp = False

        # Enemy Object Setup
        self.enemy = engine.GameObject()
        # Enemy Physics Setup
        self.enemyPhysics = engine.PhysicsComponent()
        # Enemy Transform Component
        self.enemyTransform = engine.Transform()
        self.enemy.addTransformComponent(self.enemyTransform)
        self.enemyTransform.xPos = 200
        self.enemyTransform.yPos = 100
        # Enemy Rectangle Component
        self.enemyRectangle = engine.RectangleComponent(self.enemyTransform)
        self.enemyRectangle.setDimensions(50, 50)
        self.enemyRectangle.setColor(255, 150, 150, 255)
        self.enemy.addRectangleComponent(self.enemyRectangle)
        # Enemy Tilemap Component
        self.enemy.addTileMapComponent(self.tilemap)
        # Enemy Physics Component
        self.enemy.addPhysicsComponent(self.enemyPhysics)

    # Handles player left and right movement from input
    def handlePlayerMove(self, inputs):
        if self.autoRun:
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
            return
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

    # Handles player jump logic
    def handlePlayerJump(self, inputs):
        # Increment time since space tapped
        self.timeSinceSpaceTapped += 1 / 60
        # Detect if space was tapped
        if inputs[engine.SPACE_TAPPED]:
            self.timeSinceSpaceTapped = 0
        # If space hasn't been tapped recently (wiggle room time), no jump
        if self.timeSinceSpaceTapped > self.spaceTapErrorLenience:
            return
        # If space has been tapped within the time, then perform jump if possible
        self.timeSinceSpaceTapped = 99
        if self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player):
            self.jumpSound.PlaySound()
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

    # Handles player wall climbing
    def handlePlayerWallClimbing(self, inputs, collision):
        if collision.isColliding and self.player.xVel > 0:
            # hit right wall: set xPos to correct x according to row, col
            self.playerTransform.xPos = self.tileSize * collision.firstTileColumn - self.player.mSprite.getWidth()
            # change isClimbingRight only once
            if not self.isClimbingRight:
                self.isClimbingRight = True
                # check if on ground or ceiling
                if not (self.tilemap.isOnCeiling(self.player) or self.tilemap.isOnGround(self.player)):
                    self.curYDirection *= -1
            self.isClimbingLeft = False
        elif collision.isColliding and self.player.xVel < 0:
            # hit left wall
            self.playerTransform.xPos = self.tileSize * (collision.firstTileColumn + 1)
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
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.player.xVel > 0:
                # player reached top of wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            else:
                # player is not pushing left or right
                self.player.yVel = 0
                self.curYDirection *= -1
        elif self.isClimbingLeft and not self.tilemap.isTouchingLeftWall(self.player):
            self.isClimbingLeft = False
            if self.player.xVel > 0:
                # player jumped off wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            elif self.player.xVel < 0:
                # player reached top of wall
                self.player.yVel = self.playerJumpSpeed * self.curYDirection
            else:
                # player is not pushing left or right
                self.player.yVel = 0
                self.curYDirection *= -1

    # Handles game over
    def playerGameOver(self):
        self.gameOverSound.PlaySound()
        # Reset player position
        self.playerTransform.xPos = 100
        self.playerTransform.yPos = 100
        self.camera.Update()
        self.StartGame()

    # Handles player win
    def playerWin(self):
        self.winSound.PlaySound()
        # Reset player position
        self.playerTransform.xPos = 100
        self.playerTransform.yPos = 100
        self.camera.Update()
        self.StartGame()

    # Checks for collisions with a spike (any tile with ID 10)
    def touchingSpikeCheck(self, collision):
        if self.tilemap.isTouchingType(collision, 10):
            self.playerGameOver()

    # Checks for collisions with a speed up tile (any tile with ID 42)
    def touchingSpeedUpCheck(self, collision):
        if self.tilemap.isTouchingType(collision, 42) and not self.alreadySpedUp:
            self.speedUpSound.PlaySound()
            self.alreadySpedUp = True
            self.playerRunSpeed += 3
            self.playerJumpSpeed += 3
        elif not self.tilemap.isTouchingType(collision, 42):
            self.alreadySpedUp = False

    # Checks for collisions with a spike (any tile with ID 27)
    def touchingWinCheck(self, collision):
        if self.tilemap.isTouchingType(collision, 27):
            self.playerWin()

    # Checks for collisions with the enemy
    def touchingEnemyCheck(self):
        collision = self.tilemap.checkCollision(self.enemy)
        if collision.isColliding:
            self.playerGameOver()

    # Handles all unique collision checks
    def handleCollisionTypes(self, collision):
        self.touchingEnemyCheck()
        self.touchingSpikeCheck(collision)
        self.touchingWinCheck(collision)

    # Handles all player associated updates
    def playerUpdate(self, inputs):
        # Player left and right movement
        self.handlePlayerMove(inputs)
        # Player jump
        self.handlePlayerJump(inputs)
        # Physics update on player xPos
        self.physics.UpdateX(self.player)
        # Collision update
        collision = self.tilemap.checkCollision(self.player)
        # Wall climb
        self.handlePlayerWallClimbing(inputs, collision)
        # Collision Checks
        self.handleCollisionTypes(collision)
        # Physics update on player yPos
        self.physics.UpdateY(self.player)
        # Collision update
        collision = self.tilemap.checkCollision(self.player)
        # Collision Checks
        self.handleCollisionTypes(collision)
        # Check for speedup collision
        self.touchingSpeedUpCheck(collision)
        # Ceiling or floor collision check
        if collision.isColliding and self.player.yVel < 0:
            # hit ceiling: set yPos to correct y according to row, col
            self.playerTransform.yPos = self.tileSize * (collision.firstTileRow + 1)
        elif collision.isColliding and self.player.yVel > 0:
            # hit floor
            self.playerTransform.yPos = self.tileSize * (collision.firstTileRow) - self.player.mSprite.getHeight()
        # check if off screen
        if self.playerTransform.yPos <= 0 or self.playerTransform.yPos >= self.lvlHeight - self.player.mSprite.getHeight():
            self.playerGameOver()
        
        # update frame
        if self.currentFrame >= self.currentMaxFrame:
            self.currentFrame = 0
        else:
            self.currentFrame += 1
        self.player.mSprite.update(0, 0, self.currentFrame)

    # Update
    def Update(self, inputs):
        # Quit check
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
        # Player Update
        self.playerUpdate(inputs)
        # update camera
        self.camera.Update()

    # Render
    def Render(self):
        self.sdl.clear(32, 32, 32, 255) # Set background to gray
        # TODO:
        # for entity in self.entities:
        #     entity.draw(self.sdl)
        self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.player.mSprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.enemyRectangle.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.sdl.flip()

    # Starts or re-starts the game
    def StartGame(self):
        self.playerRunSpeed = 8
        self.playerJumpSpeed = 12
        self.curYDirection = 1 # must be 1 or -1
        self.curXDirection = 1 # must be 1 or -1
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = self.playerJumpSpeed
        self.timeSinceSpaceTapped = 99
        self.alreadySpedUp = False

    # Main Loop
    def RunLoop(self):
        inputs = self.sdl.getInput()
        # self.music.PlayMusic()
        while not inputs[engine.QUIT_EVENT]:
            self.Update(inputs := self.sdl.getInput())
            self.Render()
            self.sdl.delay(25) # Needs frame rate limiting code from test_game.cpp
# Main
def main():
    game = Game(960, 540)
    game.StartGame()
    game.RunLoop()

# Run Main
if __name__ == "__main__":
    main()