#include "SurfaceResourceManager.hpp"
#include <iterator>
#include <iostream>

SurfaceResourceManager& SurfaceResourceManager::instance() {

    static SurfaceResourceManager* instance = new SurfaceResourceManager();
    return *instance;
}

void SurfaceResourceManager::shutDown() {
    std::cout << "==========" << "Commencing shutDown" << "==========" << std::endl;
    std::cout << "Freeing surfaces in resource manager..." << std::endl;
    for (auto it = mSurfaceMap.begin(); it != mSurfaceMap.end(); it++) {
        std::string filename = it->first;
        SDL_FreeSurface(it->second);
        std::cout << "Surface associated with file '" << filename << "' has been destroyed" << std::endl;
    }
    
    mSpriteSheet = nullptr;
}

SurfaceResourceManager::SurfaceResourceManager(){
}


void SurfaceResourceManager::LoadResource(std::string image_filename){

    // Create iterator for resource map
    std::unordered_map<std::string, SDL_Surface*>::const_iterator got = mSurfaceMap.find(image_filename);

    if (got == mSurfaceMap.end()) {
        // An SDL surface has not been created from the associated file...
        // It is created and inserted in the unordered map here
        std::cout << "Image filename is not in resource map...adding surface " << image_filename << " to map" << std::endl;
        SDL_Surface* newImageFilename = SDL_LoadBMP(image_filename.c_str());
        std::pair<std::string, SDL_Surface*> newPair (image_filename, newImageFilename);
        mSurfaceMap.insert(newPair);
        mSpriteSheet = newImageFilename;
    } else {
        // An SDL surface has previously been created from the associated filename.
        // mSpriteSheet is set to the surface.
        // std::cout << "Image filename " << image_filename << " located in resource map!" << std::endl;
        mSpriteSheet = got->second;
    }
}

SDL_Surface* SurfaceResourceManager::GetResource(std::string image_filename){
    // std::cout << "Retrieved saved copy of " << image_filename << " from resource map\n";
    return mSpriteSheet;
}

