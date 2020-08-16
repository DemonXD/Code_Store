#include <sstream>
#include "GameState.hpp"
#include "MainMenuState.hpp"
#include "DEFINITIONS.hpp"
#include <iostream>

namespace Sonar
{
    MainMenuState::MainMenuState(GameDataRef data): _data(data)
    {
    
    }
    void MainMenuState::Init()
    {
        _data->assets.LoadTexture("Main Menu Background",
                                  MAIN_MENU_BACKGROUND_FILEPATH);
        _data->assets.LoadTexture("Game Title",
                                  GAME_TITLE_FILEPATH);
        _data->assets.LoadTexture("Play Button",
                                  PLA_BUTTON_FILEPATH);
        _background.setTexture(this->_data->assets.GetTexture("Main Menu Background"));
        _title.setTexture(this->_data->assets.GetTexture("Game Title"));
        _playbutton.setTexture(this->_data->assets.GetTexture("Play Button"));
        _title.setPosition((SCREEN_WIDTH / 2) - (_title.
            getGlobalBounds().width / 2), _title.
            getGlobalBounds().height / 2);
        _playbutton.setPosition((SCREEN_WIDTH / 2) - (_playbutton.
            getGlobalBounds().width / 2), (SCREEN_HEIGHT / 2) - _playbutton.
            getGlobalBounds().height / 2);
    }

    void MainMenuState::HandleInput()
    {
        sf::Event event;
        while (_data->window.pollEvent(event))
        {
            if (sf::Event::Closed == event.type)
            {
                _data->window.close();
            }
            if (_data->input.IsSpriteClicked(_playbutton, sf::Mouse::Left, _data->window))
            {
                _data->machine.AddState(StateRef(new GameState(_data)), true);
            }
        }
    }
    void MainMenuState::Update(float dt)
    {
       
    }
    void MainMenuState::Draw(float dt)
    {
        _data->window.clear();
        _data->window.draw(_background);
        _data->window.draw(_title);
        _data->window.draw(_playbutton);
        _data->window.display();
    }
} // namespace Sonar
