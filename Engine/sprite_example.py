from lib import engine


class Game:

    def __init__(self, windowWidth, windowHeight):

        ###----------Same as Lucian's Game----------###
        self.sdl = engine.SDLGraphicsProgram(windowWidth, windowHeight)
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        self.player = engine.GameObject()
        self.playerRunSpeed = 15
        self.player.xVel = self.playerRunSpeed
        self.player.yVel = 0

        self.transform = engine.Transform()
        self.player.addTransformComponent(self.transform)
        #self.transform.setPosition(100, 10)
        self.transform.xPos = 100;
        self.transform.yPos = 10;
        ###-----------------------------------------###

        '''
        CREATE A SPRITE
        Spritesheets should be located in the Assets folder. Use the "loadImage"
        function to import one.
        "setRectangleDimensions" sets the size of the sprite on the screen.
        
        "setSpriteSheetDimensions" is for correctly iterating through the spritesheet.
        (width of sprite, height of sprite, max num sprites in a row, total num sprites)
        '''
        self.sprite = engine.Sprite(self.transform)
        self.sprite.setRectangleDimensions(200, 100)
        self.sprite.setSpriteSheetDimensions(200, 100, 1, 12, 0)
        self.sprite.loadImage("Assets/spritesheets/cat_right.bmp", self.sdl.getSDLRenderer())
        self.player.addSpriteComponent(self.sprite)

        self.tilemap = engine.TileMapComponent("Assets/Levels/MarioTiles/sprite_test_2.lvl")
        self.tilemap.loadTileset("Assets/tilesets/mario-like-tileset-32x32.png", self.sdl.getSDLRenderer())
        self.player.addTileMapComponent(self.tilemap)
        self.tileSize = self.tilemap.getSize()
        
        self.physics = engine.PhysicsComponent()
        self.player.addPhysicsComponent(self.physics)

        self.lvlWidth = self.tilemap.getCols() * self.tileSize
        self.lvlHeight = self.tilemap.getRows() * self.tileSize

        self.camera = engine.SpriteSideScrollerCamera(self.windowWidth, self.windowHeight, self.lvlWidth,
                                                self.lvlHeight, self.sprite)

        self.cameraOffsetX = 0
        self.cameraOffsetY = 0

        '''
        Need to keep track of number of frames in the sprite sheet. 
        '''
        self.currentFrame = 0
        self.maxFrame = 10


    def runLoop(self):
        inputs = self.sdl.getInput()
        while not inputs[engine.QUIT_EVENT]:
            self.update(inputs := self.sdl.getInput())
            self.render()
            self.sdl.delay(64)

    def update(self, inputs):
        if inputs[engine.ESCAPE_PRESSED]:
            inputs[engine.QUIT_EVENT] = True
    
        if inputs[engine.LEFT_PRESSED] or inputs[engine.A_PRESSED]:
            self.player.xVel = - self.playerRunSpeed
            self.sprite.loadImage("Assets/spritesheets/cat_left.bmp", self.sdl.getSDLRenderer())
        elif inputs[engine.RIGHT_PRESSED] or inputs[engine.D_PRESSED]:
            self.player.xVel = self.playerRunSpeed
            self.sprite.loadImage("Assets/spritesheets/cat_right.bmp", self.sdl.getSDLRenderer())

        else:
            # set x velocity to 0
            self.player.xVel = 0

        self.physics.UpdateX(self.player)

        '''
        Here we update the frame in the spritesheet. The update function (lowercase 'u') 
        does this for us. If the current frame exceend the number of frames in the spritesheet,
        reset the current frame to the first frame in the sheet.
        '''
        if self.currentFrame > self.maxFrame:
            self.currentFrame = 0
        else:
            self.currentFrame += 1
        self.sprite.update(0, 0, self.currentFrame)

        self.camera.Update()

    def render(self):
        self.sdl.clear(255, 255, 255, 255) # Set background to gray
        self.tilemap.Render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)

        '''
        Render the sprite!
        '''
        self.sprite.render(self.sdl.getSDLRenderer(), self.camera.x, self.camera.y)
        self.sdl.flip()

def main():
    game = Game(960, 540)
    game.runLoop()


if __name__ == "__main__":
    main()
