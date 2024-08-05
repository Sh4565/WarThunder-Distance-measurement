
# 
# WarThunder-Distance-measurement

[![EN](https://img.shields.io/badge/lang-EN-blue.svg)](docs/en.md)
[![RU](https://img.shields.io/badge/lang-RU-red.svg)](docs/ru.md)

## About the project
This project will help you quickly determine the distance on the mini-map in the game War Thunder.

## Compilation
___

### Cloning the repository
```shell
$ git clone https://github.com/Sh4565/WT-Distance-measurement.git
```

### Installing requirements
```shell
$ pip install -r requirements.txt
```

### Compilation
First, you need to install the [MinGW64 v12.3](https://objects.githubusercontent.com/github-production-release-asset-2e65be/220996547/86825ef3-e192-47cb-a35b-6534c686ac07?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20240803%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240803T124102Z&X-Amz-Expires=300&X-Amz-Signature=27bcd64354dac92c70216813768d49896ab4dd45b5a1daa4c3e694120fcdae69&X-Amz-SignedHeaders=host&actor_id=77664190&key_id=0&repo_id=220996547&response-content-disposition=attachment%3B%20filename%3Dwinlibs-x86_64-posix-seh-gcc-12.3.0-llvm-16.0.4-mingw-w64ucrt-11.0.0-r1.7z&response-content-type=application%2Foctet-stream)
compiler, and then run the following command:

```shell
$ python -m nuitka --standalone --mingw64 --include-data-file=./config/config.cfg=config/config.cfg --include-data-file=./config/objects.cfg=config/objects.cfg --include-data-file=./errors.log=errors.log .\src\run.py
```

## Usage
___

### Configuration
Before using, you need to configure the program. This can be done either through the configuration file .\config\config.cfg or through the program itself.
The settings include the items listed below:
```commandline
[Settings]
shooter_type = me
point_type = yellow

[Keyboard]
map_redefinition = g
close_minimap = k
update_data = l
calculating_distance = f4
```

#### Settings:
- shooter_type - shooter type [me, ally (green)],
- point_type - point type [yellow, red],
#### Keyboard:
- map_redefinition - redefine the mini-map [key name excluding Esc, Enter, and combinations]
- close_minimap - collapse the mini-map, as well as the "Back" action [key name excluding Esc, Enter, and combinations]
- update_data - update mini-map data [key name excluding Esc, Enter, and combinations]
- calculating_distance - activate distance calculation [key name excluding Esc, Enter, and combinations]

Please note that this program is still under development, so errors may occur.

### Determining the position of the mini-map
Before using, you need to determine the position of the mini-map.
To do this, go into a test flight with the following settings:
- Time of day: Day
- Weather: Clear

Then start the program and use the arrow keys and the "Enter" key to navigate to "Settings>Manual" mini-map definition.
In this mode, you need to hold down the key combination that activates the "Snipping Tool" program (Shift+Win+S) and select the area where the mini-map is located (select with margins).

After that, move the mini-map to the sky and make a few random movements until an additional mini-map window appears.
If the window appears and the mini-map is not fully displayed, then you need to press the "g" key or any other key you assigned in the map_redefinition item.

After successfully defining the mini-map, confirm the action with the "Enter" key.

### Game
In the program, select the "Game" item and enter the battle.
After loading, you need to press the "l" key or any other key you assigned in the update_data item.
After that, data on the size of the square and the mini-map window should appear in the terminal.

During the game, aim at the target, set the mark with the "f4" key (or any other key you assigned in the map_redefinition item),
and the terminal will display the distance to the target in meters. The mini-map window will also display a visual representation of the distance to the target.
