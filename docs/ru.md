
# WarThunder-Distance-measurement

[![EN](https://img.shields.io/badge/lang-EN-blue.svg)](docs/en.md)
[![RU](https://img.shields.io/badge/lang-RU-red.svg)](docs/ru.md)

## О проекте
Данный проект поможет быстро определить дистанцию по мини-карте в игре War Thunder.

## Компиляция
___

### Клонирование репозитория
```shell
git clone https://github.com/Sh4565/WT-Distance-measurement.git
```

### Установка зависимостей
```shell
pip install -r requirements.txt
```

### Компиляция
Для начала нужно установить компилятор [MinGW64 v12.3](https://objects.githubusercontent.com/github-production-release-asset-2e65be/220996547/86825ef3-e192-47cb-a35b-6534c686ac07?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20240803%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240803T124102Z&X-Amz-Expires=300&X-Amz-Signature=27bcd64354dac92c70216813768d49896ab4dd45b5a1daa4c3e694120fcdae69&X-Amz-SignedHeaders=host&actor_id=77664190&key_id=0&repo_id=220996547&response-content-disposition=attachment%3B%20filename%3Dwinlibs-x86_64-posix-seh-gcc-12.3.0-llvm-16.0.4-mingw-w64ucrt-11.0.0-r1.7z&response-content-type=application%2Foctet-stream), 
после чего нужно ввести такую команду:
```shell
python -m nuitka --standalone --mingw64 --include-data-file=./config/settings.cfg=config/settings.cfg --include-data-file=./config/objects.cfg=config/objects.cfg --include-data-file=./errors.log=errors.log .\src\run.py
```

## Использование
___

### Настройка
Перед использованием нужно настроить программу. Это можно сделать как через конфигурационный файл .\config\config.cfg, так и через саму программу.
Настройки подлежат пункты перечислены ниже:
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
- shooter_type - тип стрелка [me, ally(зеленый)],
- point_type - тип метки [yellow, red],
#### Keyboard:
- map_redefinition - переопределение мини-карты [название клавиши кроме Esc, Enter и комбинаций]
- close_minimap - свертывание мини-карты, а также действие "Назад" [название клавиши кроме Esc, Enter и комбинаций]
- update_data - обновление данных мини-карты [название клавиши кроме Esc, Enter и комбинаций]
- calculating_distance - активация расчета дистанции [название клавиши кроме Esc, Enter и комбинаций]

Учитывайте, что данная программа всё ещё находится на стадии разработки, поэтому в ней могут встречаться ошибки.

### Определение положения мини-карты
Перед использованием нужно определить положение мини-карты.
Для этого нужно зайти в пробный выезд, выбрав настройки:
- Время суток: День
- Погода: Ясно

После этого запустите программу и при помощи стрелок и клавиши "Enter" перейдите в "Настройки>Ручное" определение мини-карты.
В этом режиме вам нужно зажать комбинацию клавиш, активирующую программу "Ножницы" (Shift+Win+S), и выделить область, где находится мини-карта (выделять нужно с зазорами).

После этого нужно навести мини-карту на небо и сделать пару произвольных движений, пока не появится дополнительное окно мини-карты.
Если окно появилось, а мини-карта отображается не полностью, тогда нужно нажать клавишу "g" или любую другую, которую вы назначили в пункте map_redefinition.

После успешного определения мини-карты подтвердите действие клавишей "Enter".

### Игра
В программе выберите пункт "Игра" и зайдите в бой.
После загрузки нужно нажать клавишу "l" или любую другую, которую вы назначили в пункте update_data.
После этого в терминале должны появиться данные о размере квадрата и окно мини-карты.

В процессе игры наведите курсор на цель, поставьте метку клавишей "f4" (или любую другую, которую вы назначили в пункте map_redefinition),
и в терминале появится дистанция до цели в метрах. Также в окне мини-карты будет визуальное отображение с дистанцией до цели.
