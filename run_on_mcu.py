"""Gets the path to the compiled programs, and automatically runs these on
the MCUs."""
from subprocess import run
from subprocess import check_output 
from subprocess import Popen, PIPE
from pathlib import Path
import pyautogui
from fcntl import fcntl, F_GETFL, F_SETFL
import time
import os
from os import O_NONBLOCK
import shutil

VOLUMES_MNT = '/Volumes/NODE_F767ZI'
MODEL_FOLDER = Path.cwd() / 'train' / 'models'


def main():
    model_inftime_map = {}
    model_path = MODEL_FOLDER
    folders = list(model_path.glob("*"))
    for folder in folders:
        models = list(folder.glob('*.bin'))
        if not models:
            print("No binary detected here.")
        
        model = models[0]
        print(f"Going to work on {model}")
        # Copy the model over, and wait for some time for the utility
        # to flash the model over to the board.
        time.sleep(5.0)
        shutil.copy(model, VOLUMES_MNT)
        time.sleep(30.0)
        print("Going to query mbed for the inference time")
        process = Popen(['python3', 'get_inf_time.py'], stdout=PIPE)
        out, _ = process.communicate()
        out = eval(out.decode('utf-8'))
        model_inftime_map[model] = out

    print(model_inftime_map)


if __name__ == '__main__':
    main()
