# pyc-man
Pygame PAC MAN

Simple [PAC-MAN](https://www.gamasutra.com/view/feature/3938/the_pacman_dossier.php?print=1) clone.
 - Use arrows to move.
 - Eat Energizers to scare ghosts.
 - Ghosts speed up with each level.
 - Dumb AI, only Blinky :(

__Sources:__
- Phaser spriteshhets for pacman [assets](http://labs.phaser.io/assets/games/pacman/).
- Gamasutra [article](https://www.gamasutra.com/view/feature/3938/the_pacman_dossier.php?print=1) on intricate details of pacman that are mostly irrelevant to this build.
 
Элементарный клон игры [PAC-MAN](https://ru.wikipedia.org/wiki/Pac-Man)
 - Используйте стрелки для управления.
 - Съешьте большие точки чтобы напугать призрака.
 - Противники ускоряются с каждой победой.
 - Простой ИИ, только один призрак :(  

### Информация для проверяющих
В приложении используются файлы формата Tiled(xml) для создания и загрузки уровня.
pytmx - библиотека, которая позволяет загружать такие уровни.

Кроме уровней формат Tiled используется для хранения спрайтовых анимаций и графического шрифта.

SpriteFactory и AnimationFactory - создают статические спрайты и анимированные спрайты на основе таких файлов.
BMPFont - загружает из файла шрифт и позволяет рисовать с его помощью строки.

В корневой директории лежат файлы основного движка, без привязки к конкретной игре.
В теории, на этих примерах дети могут построить любую игру с взаимодействующими персонажами.
В папке pyc_man лежат файлы с логикой конкретной игры.
 
Комментариев нет ¯\\\_(ツ)_/¯

__TODO:__
 - отловить проблему при переключении звука (иногда пропадает один из каналов);
 - добавить логику при смерти призрака; 
 - добавить остальных призраков;
 - реализовать состояние игры Scatter;
 - добавить изменение скорости движения в процесее игры;
 - оформить код в модуль;
 - вынести константы в файл конфигурации, избавившись от статических зависимостей.

