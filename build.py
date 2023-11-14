import sys
from pathlib import Path
from PyInstaller.__main__ import run

if __name__ == '__main__':
    game_folder = '.'  
    spec_file = 'game.spec'

    run(['--name=Dorom', '--onefile', '--noconsole', '--add-data=' + game_folder + ';.', game_folder + '/main.py'])

    spec_path = Path('dist') / spec_file
    spec_path.replace(spec_file)
