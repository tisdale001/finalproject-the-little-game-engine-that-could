#pragma once

#include <memory>
#include <cstdint>

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

#include "Transform.hpp"

// TODO: setImage function?
class RectangleComponent {
    public:
        RectangleComponent(Transform* transform);

        ~RectangleComponent();

        void Update();

        void Render(std::uintptr_t rendererAddress, int camOffsetX, int camOffsetY);

        void setDimensions(int w, int h);

        void setColor(int r, int g, int b, int a);

        int getWidth();

        int getHeight();

        int getX();

        int getY();

        int getCenterX();

        int getCenterY();

    private:
        int width;
        int height;
        int redValue;
        int greenValue;
        int blueValue;
        int alphaValue;
        Transform* transform;
};
