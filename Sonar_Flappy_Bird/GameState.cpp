#include <sstream>
#include "GameOverState.hpp"
#include "GameState.hpp"
#include "MainMenuState.hpp"
#include "DEFINITIONS.hpp"
#include <iostream>
#include <fstream>

namespace Sonar
{
    GameState::GameState(GameDataRef data): _data(data)
    {
    
    }
    void GameState::Init()
    {
        _data->assets.LoadTexture("Game Backgroud", GAME_BACKGROUND_FILEPATH);
        _data->assets.LoadTexture("Pipe Up", PIPE_UP_FILEPATH);
        _data->assets.LoadTexture("Pipe Down", PIPE_DOWN_FILEPATH);
        _data->assets.LoadTexture("Land", LAND_FILEPATH);
        _data->assets.LoadTexture("Bird Frame 1", BIRD_FRAME_1_FILEPATH);
        _data->assets.LoadTexture("Bird Frame 2", BIRD_FRAME_2_FILEPATH);
        _data->assets.LoadTexture("Bird Frame 3", BIRD_FRAME_3_FILEPATH);
        _data->assets.LoadTexture("Bird Frame 4", BIRD_FRAME_4_FILEPATH);
        _data->assets.LoadTexture("Scoring Pipe", SCORING_PIPE_FILEPATH);
        _data->assets.LoadFont("Flappy Font", FLAPPY_FONT_FILEPATH);

        pipe = new Pipe(_data);
        land = new Land(_data);
        bird = new Bird(_data);
        flash = new Flash(_data);
        hud = new HUD(_data);

        _background.setTexture(this->_data->assets.GetTexture("Game Backgroud"));

        _gameState = GameStates::eReady;
        _score = 0;
        hud->UpdateScore(_score);
        _gameState = GameStates::eReady;
    }

    void GameState::HandleInput()
    {
        sf::Event event;
        while (_data->window.pollEvent(event))
        {
            if (sf::Event::Closed == event.type)
            {
                _data->window.close();
            }
            if (_data->input.IsSpriteClicked(_background, sf::Mouse::Left, _data->window))
            {
                if (GameStates::eGameOver != _gameState)
                {
                    _gameState = GameStates::ePlaying;
                    bird->Tap();
                }
            }
        }
    }
    void GameState::Update(float dt)
    {
        if (GameStates::eGameOver != _gameState)
        {
            bird->Animate(dt);
            land->MoveLand(dt);
        }
        if (GameStates::ePlaying == _gameState)
        {
            pipe->MovePipes(dt);
            if (clock.getElapsedTime().asSeconds() > PIPE_SPAWN_FREQUENCY)
            {
                pipe->RandomisePipeOffset();
                pipe->SpawnInvisiblePipe();
                pipe->SpawnBottomPipe();
                pipe->SpawnTopPipe();
                pipe->SpawnScoringPipe();
                clock.restart();
            }
            bird->Update(dt);
            std::vector<sf::Sprite> landSprites = land->GetSprites();
            for (std::vector<sf::Sprite>::size_type i = 0; i < landSprites.size();i++)
            {
                if (collision.CheckSpriteCollision(
                        bird->GetSprite(), 0.7f,
                        landSprites.at(i), 1.0f))
                {
                    _gameState = GameStates::eGameOver;
                    clock.restart();
                }
            }
            std::vector<sf::Sprite> pipeSprites = pipe->GetSprites();
            for (std::vector<sf::Sprite>::size_type i = 0; i < pipeSprites.size();i++)
            {
                if (collision.CheckSpriteCollision(
                    bird->GetSprite(), 0.625f,
                    pipeSprites.at(i), 1.0f))
                {
                    _gameState = GameStates::eGameOver;
                    clock.restart();
                }
            }

            //  计分
            
            if (GameStates::ePlaying == _gameState)
            {
                std::vector<sf::Sprite> &scoringSprites = pipe->GetScoringSprites();
                for (std::vector<sf::Sprite>::size_type i = 0; i < scoringSprites.size();i++)
                {
                    if (collision.CheckSpriteCollision(
                        bird->GetSprite(), 0.625f,
                        pipeSprites.at(i), 1.0f))
                    {
                        _score++;
                        hud->UpdateScore(_score);
                        scoringSprites.erase(scoringSprites.begin() + i);
                    }
                }
            }
            
        }
        if (GameStates::eGameOver == _gameState)
        {
            flash->Show(dt);
        }
    }
    void GameState::Draw(float dt)
    {
        this->_data->window.clear();
        this->_data->window.draw(_background);
        pipe->DrawPipes();
        land->DrawLand();
        bird->Draw();
        flash->Draw();
        hud->Draw();
        this->_data->window.display();
    }
} // namespace Sonar
