#ifndef SURFACE_RESOURCE_MANAGER_HPP
#define SURFACE_RESOURCE_MANAGER_HPP

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
#else // This works for Mac
    #include <SDL.h>
#endif

// I recommend a map for filling in the resource manager
#include <unordered_map>
#include <string>

class SurfaceResourceManager{
public:

    static SurfaceResourceManager& instance();

    void shutDown();
    
    // TODO: Refactor to be a static function
    void LoadResource(std::string image_filename);
    // TODO: Refactor to be a static function
    SDL_Surface* GetResource(std::string image_filename);

private:
    // Private constructor
    SurfaceResourceManager();

    std::unordered_map<std::string, SDL_Surface*> mSurfaceMap;

    SDL_Surface* mSpriteSheet;
};


#endif