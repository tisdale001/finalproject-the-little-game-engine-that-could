#include "SoundResourceManager.hpp"
#include <iterator>
#include <iostream>

SoundResourceManager& SoundResourceManager::instance() {

    static SoundResourceManager* instance = new SoundResourceManager();
    return *instance;
}

void SoundResourceManager::shutDown() {
    std::cout << "==========" << "Commencing shutDown" << "==========" << std::endl;
    std::cout << "Freeing sounds in resource manager..." << std::endl;
    for (auto it = mSoundMap.begin(); it != mSoundMap.end(); it++) {
        char* chunk = it->first;
        Mix_FreeChunk(it->second);
        std::cout << "Sound associated with char* '" << chunk << "' has been destroyed" << std::endl;
    }

    // Mix_Quit();      // Should this be here?
    
    mSound = nullptr;
}

SoundResourceManager::SoundResourceManager(){
}


void SoundResourceManager::LoadResource(char* fileName){

    // Create iterator for resource map
    std::unordered_map<char*, Mix_Chunk*>::const_iterator got = mSoundMap.find(fileName);

    if (got == mSoundMap.end()) {
        std::cout << "Sound name is not in resource map...adding sound " << fileName << " to map" << std::endl;
        Mix_Chunk* sound = Mix_LoadWAV(fileName);
        if(sound == NULL)
        {
            printf("Failed to load sound! SDL_mixer Error: %s\n", Mix_GetError());
        }
        std::pair<char*, Mix_Chunk*> newPair (fileName, sound);
        mSoundMap.insert(newPair);
        mSound = sound;
    } else {
        // An SDL surface has previously been created from the associated filename.
        // mSpriteSheet is set to the surface.
        std::cout << "Sound " << fileName << " located in resource map!" << std::endl;
        mSound = got->second;
    }
}

Mix_Chunk* SoundResourceManager::GetResource(char* fileName){
    std::cout << "Retrieved saved copy of " << fileName << " from sound resource map\n";
    return mSound;
}