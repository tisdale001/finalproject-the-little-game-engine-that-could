#include "GameObject.hpp"

/** @brief Constructor which takes in an std::uintptr_t for a renderer
*
* Overloaded Constructor which takes in an address to an existing renderer
*
*/
GameObject::GameObject(std::uintptr_t rendererAddress) {
    mRenderer = rendererAddress;
}
/** @brief Constructor
 * 
 * Simple Constructor: no params
*/
GameObject::GameObject() {}

/** @brief Deconstructor
 * 
*/
GameObject::~GameObject() {}

/** @brief Empty method for now
 * 
*/
void GameObject::Update() {
    // TODO: check collision in between?
    // TODO: update physics?
    // if (mPhysicsComponent != nullptr) {
    //     mPhysicsComponent->Update(*this);
    // }
}

/** @brief Render calls Render() for mRectangle and mTileMapComponent
 * 
 * Render calls Render() for mRectangle and mTileMapComponent according to camera offset
*/
void GameObject::Render(std::uintptr_t rendererAddress) { // TODO: Figure out why we can't use
    if (mCamera != nullptr) {
        if (mRectangle != nullptr) {
            mRectangle->Render(rendererAddress, mCamera->GetXOffset(), mCamera->GetYOffset());
        }
        if (mTileMapComponent != nullptr) {
            mTileMapComponent->Render(rendererAddress, mCamera->GetXOffset(), mCamera->GetYOffset());
        }
        if (mSprite != nullptr) {
            mSprite->render(rendererAddress, mCamera->GetXOffset(), mCamera->GetYOffset());
        }
    }
}

// TODO: addComponent functions are temporary, we should use a template function
// to replace this or maybe a map?
/** @brief Adds Transform component
 * 
 * Adds pre-existing Transform component to GameObject as mTransform
*/
void GameObject::addTransformComponent(Transform* transform) {
    mTransform = transform;
}

/** @brief Adds RectangleComponent
 * 
 * Adds pre-existing RectangleComponent to GameObject as mRectangle. Used instead of sprite in early development.
*/
void GameObject::addRectangleComponent(RectangleComponent* rectangle) {
    mRectangle = rectangle;
}

/** @brief Adds PhysicsComponent
 * 
 * Adds PhysicsComponent to GameObject as mPhysicsComponent
*/
void GameObject::addPhysicsComponent(PhysicsComponent* physicsComponent) {
    mPhysicsComponent = physicsComponent;
}

/** @brief Adds TileMapComponent
 * 
 * Adds TileMapComponent to GameObject as mTileMapComponent
*/
void GameObject::addTileMapComponent(TileMapComponent* tileMapComponent) {
// void GameObject::addTileMapComponent(std::shared_ptr<TileMapComponent> tileMapComponent) {
    mTileMapComponent = tileMapComponent;
}

/** @brief Adds Camera
 * 
 * Adds camera to GameObject as mCamera
*/
void GameObject::addCamera(ICamera* camera) {
    mCamera = camera;
}

void GameObject::addSpriteComponent(Sprite *sprite) {
    mSprite = sprite;
}