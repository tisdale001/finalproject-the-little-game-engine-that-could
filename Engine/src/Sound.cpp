#include "Sound.hpp"

Sound::Sound() {
    if(Mix_OpenAudio( 44100, MIX_DEFAULT_FORMAT, 2, 2048 ) < 0)
	{
		printf("Sound could not initialize! SDL_mixer Error: %s\n", Mix_GetError());
	}
}

Sound::~Sound() {
    Mix_Quit();
}

void Sound::SetSound(char* fileName) {
    //Load sound effects
	soundFile = Mix_LoadWAV(fileName);
	if(soundFile == NULL)
	{
		printf("Failed to load sound! SDL_mixer Error: %s\n", Mix_GetError());
	}
}

void Sound::PlaySound() {
    if(soundFile != NULL)
	{
        Mix_PlayChannel( -1, soundFile, 0 );
	}
}