#include "Music.hpp"

Music::Music() {
    if(Mix_OpenAudio( 44100, MIX_DEFAULT_FORMAT, 2, 2048 ) < 0)
	{
		printf("Music could not initialize! SDL_mixer Error: %s\n", Mix_GetError());
	}
}

Music::~Music() {
    Mix_Quit();
}

void Music::SetMusic(char* fileName) {
    //Load Music effects
	musicFile = Mix_LoadMUS(fileName);
	if(musicFile == NULL)
	{
		printf("Failed to load music! SDL_mixer Error: %s\n", Mix_GetError());
	}
}

void Music::PlayMusic() {
    if(musicFile != NULL)
	{
        Mix_PlayMusic(musicFile, -1);
	}
}

void Music::PauseMusic() {
    if(musicFile != NULL)
	{
        Mix_PauseMusic();
	}
}

void Music::UnPauseMusic() {
    if(musicFile != NULL)
	{
        Mix_ResumeMusic();
	}
}

void Music::StopMusic() {
    if(musicFile != NULL)
	{
        Mix_HaltMusic();
	}
}