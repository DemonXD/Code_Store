#pragma once

#include <SFML/Graphics.hpp>
#include "State.hpp"
#include "Game.hpp"
#include "Pipe.hpp"
#include "Land.hpp"
#include "Bird.hpp"
#include "Collision.hpp"
#include "Flash.hpp"
#include "HUD.hpp"

namespace Sonar
{
    class GameState: public State
    {
    public:
        GameState(GameDataRef data);
        void Init();
        void HandleInput();
        void Update(float dt);
        void Draw(float dt);
    private:
        GameDataRef _data;
        sf::Sprite _background;
        Pipe *pipe;
        sf::Clock clock;
        Land *land;
        Bird *bird;
        Flash *flash;
        HUD *hud;
        Collision collision;
        int _gameState;
        int _score;
    };
}