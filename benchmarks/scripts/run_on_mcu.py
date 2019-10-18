"""Gets the path to the compiled programs, and automatically runs these on
the MCUs."""
from subprocess import PIPE, Popen
from threading  import Thread
from queue import Queue
import subprocess
from subprocess import run
from subprocess import check_output 
from subprocess import Popen, PIPE
from pathlib import Path
import glob
from fcntl import fcntl, F_GETFL, F_SETFL
import time
import os
from os import O_NONBLOCK
import shutil
import argparse
import git

def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root

parser = argparse.ArgumentParser()

parser.add_argument("--target", default=None, required=True)
parser.add_argument("--timelimit", default=10, type=int)
parser.add_argument("--output_path", default="mbed_output")
args = parser.parse_args()

def get_volume():
    #x3'/Volumes/NODE_F767ZI'
    target_volume = [x for x in glob.glob("/Volumes/*") if "NODE_" in x]
    # For linux, it might be in media
    target_volume += list(Path('/media').rglob("*NODE*"))
    return target_volume[0]

project_base_dir = get_git_root(os.path.dirname(os.path.abspath(__file__))) 
VOLUMES_MNT = get_volume()
MODEL_FOLDER = Path(args.target)

def main():    
    model_path = MODEL_FOLDER
    files = list(model_path.glob("*.bin"))
    # print(model_path)
    # print(files)
    binaries = []
    for file in files:
        if ".bin" in str(file):
            binaries.append(file)
            pass
        
        model = binaries[0]        
        print("Going to work on {}".format(model))
        # Copy the model over, and wait for some time for the utility
        # to flash the model over to the board.        
        time.sleep(10.0)
        shutil.copy(str(model), str(VOLUMES_MNT))
        time.sleep(30.0)
        
        # Run the binary
        print("Running binary")
        a = subprocess.Popen(['mbed sterm -r'],
                             stdout=subprocess.PIPE,
                             shell=True)

        flags = fcntl(a.stdout, F_GETFL) # get current p.stdout flags
        fcntl(a.stdout, F_SETFL, flags | O_NONBLOCK)

        print("Reading lines")
        #time.sleep(args.timelimit)
       
        out = None
        lines = []
        t = time.time()
        while True:
            print("Iterating lines...")
            while True:
                try:
                    line = os.read(a.stdout.fileno(), 1024)
                    lines.append(line)
                    if len(line) == 0:
                        break
                except OSError:
                    break
            print("Got: ", lines)
            time.sleep(1)
            if time.time()-t >= args.timelimit:
                break
        
        time.sleep(0.5)
        a.kill()
        time.sleep(0.5)
        a.kill()
        
        print("Writing lines")
        lines = [x for x in lines if x.decode("utf-8").strip() != ""]
        print(lines)
        with open(args.output_path, "w") as f:
            f.write("".join([x.decode("utf-8") for x in lines]))

        # Hack to only eval 1 binary
        break


if __name__ == '__main__':
    main()
