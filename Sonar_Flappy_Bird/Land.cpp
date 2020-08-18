#include "Land.hpp"
#include "DEFINITIONS.hpp"


namespace Sonar
{
    Land::Land(GameDataRef data): _data(data)
    {
        sf::Sprite sprite(_data->assets.GetTexture("Land"));
        sf::Sprite sprite2(_data->assets.GetTexture("Land"));
        sprite.setPosition(0, _data->window.getSize().y - sprite.
            getGlobalBounds().height);
        sprite2.setPosition(sprite.getGlobalBounds().width, _data->window
            .getSize().y - sprite2.getGlobalBounds().height);

        _landSprites.push_back(sprite);
        _landSprites.push_back(sprite2);
    }
    void Land::MoveLand(float dt)
    {
        for (unsigned short int i = 0; i < _landSprites.size(); i++)
        {
            float movement = PIPE_MOVEMENT_SPEED * dt;
            _landSprites.at(i).move(-movement, 0.0f);
            if (_landSprites.at(i).getPosition().x < 0 - _landSprites.at(i).getGlobalBounds().width)
            {
                sf::Vector2f position(_data->window.getSize().x, _landSprites.at(i).getPosition().y);
                _landSprites.at(i).setPosition(position);
            }
    }
    }

    void Land::DrawLand()
    {
        for (unsigned short int i = 0; i < _landSprites.size(); i++)
        {
            _data->window.draw(_landSprites.at(i));
        }
    }
    const std::vector<sf::Sprite> &Land::GetSprites() const
    {
        return _landSprites;
    }

}