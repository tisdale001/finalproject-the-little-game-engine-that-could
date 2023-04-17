#ifndef SOUND_RESOURCE_MANAGER_HPP
#define SOUND_RESOURCE_MANAGER_HPP

#if defined(LINUX) || defined(MINGW)
    #include <SDL2/SDL.h>
    #include <SDL2/SDL_mixer.h>
#else // This works for Mac
    #include <SDL.h>
    #include <SDL_mixer.h>
#endif

#include <unordered_map>

class SoundResourceManager{
    public:

        static SoundResourceManager& instance();

        void shutDown();
        
        // TODO: Refactor to be a static function
        void LoadResource(char* fileName);
        // TODO: Refactor to be a static function
        Mix_Chunk* GetResource(char* fileName);

    private:
        // Private constructor
        SoundResourceManager();

        std::unordered_map<char*, Mix_Chunk*> mSoundMap;

        Mix_Chunk* mSound;
};


#endif