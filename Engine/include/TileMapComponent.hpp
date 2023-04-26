#pragma once

#include <iostream>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>
#include <algorithm>

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

#include "GameObject.hpp"

struct Collision {
    bool isColliding;
    int firstTileRow;
    int firstTileColumn;
    int firstTileID;
    std::vector<int> allTileTypes;
};

class TileMapComponent {
    public:
        TileMapComponent(const std::string& levelPath);

        TileMapComponent(int rows, int cols, int size);

        ~TileMapComponent();

        void ExtendTilemap(const std::string& levelPath);

        void Render(std::uintptr_t rendererAddress, int offsetX, int offsetY);

        Collision checkCollision(GameObject* o);

        bool isOnGround(GameObject* o);

        bool isOnCeiling(GameObject * o);

        bool isTouchingRightWall(GameObject* o);

        bool isTouchingLeftWall(GameObject* o);

        bool isTouchingType(Collision collision, int id);

        int getRows();

        int getCols();

        int getSize();

        void loadTileset(std::string tilesetPath, std::uintptr_t rendererAddress);

        void PrintTiles();

        bool isValidTile(int row, int col);

        // Return type of tile at row and col
        int tileAt(int row, int col);

        // Return type of tile at coordinate
        int tileAtXY(int x, int y);

        // Get tile idx in mTiles
        int getTileIdx(int row, int col);

        void setTile(int row, int col, int type);

    private:
        int mRows;
        int mCols;
        int mSize;
        int mTilesetRows;
        int mTilesetCols;
        std::vector<int> mTiles;
        SDL_Texture* tilesetTexture;
};
