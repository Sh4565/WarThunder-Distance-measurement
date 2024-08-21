
import os
import sys
import argparse

from pathlib import Path


def module_to_pofile(path, output_path=''):
    workdir = Path(path).resolve()

    files = []
    for file in workdir.iterdir():
        if file.suffix == '.py':
            files.append(file)

    command = 'xgettext -d messages'
    for file in files:
        command += f' "{file}"'

    output_file = Path(output_path).resolve() if output_path else workdir
    command += f' -o "{output_file / workdir.stem}.pot"'

    os.system(command)


def main():
    module_to_pofile(Path('src', 'cli'), 'locales')


if __name__ == '__main__':
    main()
