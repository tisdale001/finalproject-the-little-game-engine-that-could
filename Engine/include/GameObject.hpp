#pragma once

#include <memory>
#include <cstdint>
#include <iostream>

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

#include "ICamera.hpp"
#include "Transform.hpp"
#include "Rectangle.hpp"
#include "PhysicsComponent.hpp"
#include "TileMapComponent.hpp"
#include "Sprite.hpp"

class TileMapComponent;

class GameObject {
    public:

        GameObject(std::uintptr_t rendererAddress);
        
        GameObject();

        ~GameObject();

        void Update();

        void Render(std::uintptr_t rendererAddress);

        void addTransformComponent(Transform* transform);
        void addRectangleComponent(RectangleComponent* rectangle);
        void addPhysicsComponent(PhysicsComponent* physicsComponent);
        void addTileMapComponent(TileMapComponent* tileMapComponent);
        void addSpriteComponent(Sprite *sprite);
        void addCamera(ICamera* camera);

        Transform* mTransform = nullptr;
        RectangleComponent* mRectangle = nullptr;
        PhysicsComponent* mPhysicsComponent = nullptr;
        TileMapComponent* mTileMapComponent = nullptr;
        Sprite* mSprite = nullptr;
        ICamera* mCamera = nullptr;
        std::uintptr_t mRenderer;
        int xVel = 0;
        int yVel = 0;
};
