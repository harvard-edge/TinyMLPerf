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
            continue
        
        model = models[0]
        print(f"Going to work on {model}")
        # Copy the model over, and wait for some time for the utility
        # to flash the model over to the board.
        time.sleep(10.0)
        shutil.copy(model, VOLUMES_MNT)
        time.sleep(40.0)
        
        out = None
        num_tries = 0
        while out is None and num_tries < 4:
            print("Going to query mbed for the inference time, try {}".format(num_tries))
            process = Popen(['python3', 'get_inf_time.py'], stdout=PIPE)
            out, _ = process.communicate()
            out = eval(out.decode('utf-8'))
            logfile = Path.cwd() / 'log.log'
            print(out)
            num_tries += 1

        with logfile.open('a') as f:
            f.write("{},{}\n".format(str(model), out))
        model_inftime_map[model] = out

    print(model_inftime_map)


if __name__ == '__main__':
    main()
