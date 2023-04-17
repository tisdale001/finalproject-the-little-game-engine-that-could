#include "TextureResourceManager.hpp"
#include <iterator>
#include <iostream>

TextureResourceManager& TextureResourceManager::instance() {

    static TextureResourceManager* instance = new TextureResourceManager();
    return *instance;
}

void TextureResourceManager::shutDown() {
    std::cout << "==========" << "Commencing shutDown" << "==========" << std::endl;
    std::cout << "Freeing textures in resource manager..." << std::endl;
    for (auto it = mTextureMap.begin(); it != mTextureMap.end(); it++) {
        SDL_Surface* surf = it->first;
        SDL_DestroyTexture(it->second);
        std::cout << "Texture associated with surface '" << surf << "' has been destroyed" << std::endl;
    }
    
    mTexture = nullptr;
}

TextureResourceManager::TextureResourceManager(){
}


void TextureResourceManager::LoadResource(SDL_Surface* surface, SDL_Renderer* renderer){

    // Create iterator for resource map
    std::unordered_map<SDL_Surface*, SDL_Texture*>::const_iterator got = mTextureMap.find(surface);

    if (got == mTextureMap.end()) {
        // An SDL surface has not been created from the associated file...
        // It is created and inserted in the unordered map here
        std::cout << "Texture name is not in resource map...adding texture " << surface << " to map" << std::endl;
        SDL_Texture* text = SDL_CreateTextureFromSurface(renderer, surface);
        std::pair<SDL_Surface*, SDL_Texture*> newPair (surface, text);
        mTextureMap.insert(newPair);
        mTexture = text;
    } else {
        // An SDL surface has previously been created from the associated filename.
        // mSpriteSheet is set to the surface.
        // std::cout << "Surface " << surface << " located in resource map!" << std::endl;
        mTexture = got->second;
    }
}

SDL_Texture* TextureResourceManager::GetResource(SDL_Surface* surface){
    // std::cout << "Retrieved saved copy of " << surface << " from texture resource map\n";
    return mTexture;
}
