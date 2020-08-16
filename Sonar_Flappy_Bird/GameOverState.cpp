#include <sstream>
#include "GameOverState.hpp"
#include "MainMenuState.hpp"
#include "DEFINITIONS.hpp"
#include <iostream>

namespace Sonar
{
    GameOverState::GameOverState(GameDataRef data): _data(data)
    {
    
    }
    void GameOverState::Init()
    {
        _data->assets.LoadTexture("Game Over Backgroud",
                                  GAME_OVER_BACKGROUND_FILEPATH);
        _background.setTexture(this->_data->assets.GetTexture("Game Over Backgroud"));
    }

    void GameOverState::HandleInput()
    {
        sf::Event event;
        while (_data->window.pollEvent(event))
        {
            if (sf::Event::Closed == event.type)
            {
                _data->window.close();
            }
        }
    }
    void GameOverState::Update(float dt)
    {

    }
    void GameOverState::Draw(float dt)
    {
        _data->window.clear();
        _data->window.draw(_background);
        _data->window.display();
    }
} // namespace Sonar
