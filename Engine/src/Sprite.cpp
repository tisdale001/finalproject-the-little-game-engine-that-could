#include "Sprite.hpp"
#include "SurfaceResourceManager.hpp"
#include "TextureResourceManager.hpp"

Sprite::Sprite(Transform* _transform, bool readLeftToRight){
    mTransform = _transform;
    mReadLeftToRight = readLeftToRight;
}

Sprite::~Sprite(){
}

// Set the sprite position
void Sprite::setPosition(int x, int y){
    mPositionX = x;
    mPositionY = y;
}

void Sprite::update (int x, int y, int frame){
    // The part of the image that we want to render
    mCurrentFrame = frame;
    if(mCurrentFrame>mLastFrame){
        mCurrentFrame=0;
    }

    if (mReadLeftToRight) {
        mSrc.y = floor(mCurrentFrame / mNumSpritesInRow) * mSrc.h;
        mSrc.x = (mCurrentFrame % mNumSpritesInRow) * (mSrc.w + mNumPixelsToTrimFromWidth);
    }
    else {
        mSrc.y = floor(mCurrentFrame / mNumSpritesInRow) * mSrc.h;
        mSrc.x = mTextureWidth - ((mCurrentFrame % mNumSpritesInRow) * (mSrc.w + mNumPixelsToTrimFromWidth) - mNumPixelsToTrimFromWidth);
    }
    
}

void Sprite::render(std::uintptr_t rendererAddress, int camOffsetX, int camOffsetY){
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    mDest.x = mTransform->xPos - camOffsetX;
    mDest.y = mTransform->yPos - camOffsetY;
    SDL_RenderCopy(renderer, mTexture, &mSrc, &mDest);
    // std::cout << "Pos: " << mPosition.x << "  Des: " << mDest.x << std::endl;
}

void Sprite::loadImage(std::string filePath, std::uintptr_t rendererAddress){
    SDL_Renderer* renderer = reinterpret_cast<SDL_Renderer*>(rendererAddress);
    SurfaceResourceManager::instance().LoadResource(filePath);
    SDL_Surface* mSpriteSheet = SurfaceResourceManager::instance().GetResource(filePath);
    if(nullptr == mSpriteSheet){
           SDL_Log("Failed to allocate surface");
    }else{
        // SDL_Log("Allocated a bunch of memory to create identical game character");
        // Create a texture from our surface
        // Textures run faster and take advantage 
        // of hardware acceleration
        TextureResourceManager::instance().LoadResource(mSpriteSheet, renderer);
        mTexture = TextureResourceManager::instance().GetResource(mSpriteSheet); //SDL_CreateTextureFromSurface(renderer, mSpriteSheet);
        SDL_Point size;
        SDL_QueryTexture(mTexture, NULL, NULL, &size.x, &size.y);
        mTextureWidth = size.x;
        mTextureHeight = size.y;
        
    }
}

void Sprite::setSpriteSheetDimensions(int frameWidth, int frameHeight, int numSpritesInRow, unsigned int totalSprites, unsigned int numPixelsToTrimFromWidth) {

    mLastFrame = totalSprites;
    mNumPixelsToTrimFromWidth = numPixelsToTrimFromWidth;
    mSrc.w = frameWidth - numPixelsToTrimFromWidth;
    mSrc.h = frameHeight;
    mNumSpritesInRow = numSpritesInRow;
}

void Sprite::setRectangleDimensions(int x, int y) {

    mDest.w = x;
    mDest.h = y;
}

int Sprite::send() {
    return 0;
}

void Sprite::receive(int val) {

    mPositionX += val;
}

void Sprite::identify () {
    std::cout << "Sprite" << std::endl;
}

int Sprite::getWidth() {

    return mDest.w;
}

int Sprite::getHeight() {

    return mDest.h;
}

int Sprite::getX() {
    
    return mTransform->xPos;
}

int Sprite::getY() {

    return mTransform->yPos;
}

int Sprite::getCenterX() {

    return mTransform->xPos + mDest.w / 2;
}

int Sprite::getCenterY() {

    return mTransform->yPos + mDest.h / 2;
}