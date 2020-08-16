#pragma once

#include <SFML/Graphics.hpp>


namespace Sonar
{
    class Collision // 碰撞检测
    {
        public:
            Collision();
            // 粗略的检测
            // bool CheckSpriteCollision(
            //     sf::Sprite sprite1, sf::Sprite sprite2);
            // 有附加值的检测
            bool CheckSpriteCollision(
                sf::Sprite sprite1, float scale1,
                sf::Sprite sprite2, float scale2);
    };

} // namespace Sonar