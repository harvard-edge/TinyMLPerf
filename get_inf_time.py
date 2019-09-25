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


def get_inference_time_from_mbed(mbed_sleep=4.0, inf_sleep=5.0):
    # First do some sanity checks on whether or not the MCU is connected
    a = Popen(['mbed', 'sterm'], stdout=PIPE)
    flags = fcntl(a.stdout, F_GETFL) # get current p.stdout flags
    fcntl(a.stdout, F_SETFL, flags | O_NONBLOCK)
    time.sleep(mbed_sleep)
    # Biggest hack, literally simulating the control b options haha
    pyautogui.hotkey('ctrl', 'b')
    pyautogui.hotkey('ctrl', 'b')
    lines = []
    time.sleep(inf_sleep)
    while True:
        try:
            line = os.read(a.stdout.fileno(), 1024)
            lines.append(line)
            if len(line) == 0:
                break
        except OSError:
            # the os throws an exception if there is no data
            break
    time.sleep(0.5)
    a.kill()
    time.sleep(0.5)
    a.kill()
    
    for line in lines:
        if 'microseconds' in line.decode('utf-8'):
            report = line.decode('utf-8')
            fps = float(report.strip().split()[-1])
            return fps
    
    # Return none if we couldn't find a line with inference in it.
    return None


def main():
    print(get_inference_time_from_mbed())


if __name__ == '__main__':
    main()
