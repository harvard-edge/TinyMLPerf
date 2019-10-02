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
parser.add_argument("--timelimit", default=60)
parser.add_argument("--output_path", default="mbed_output")
args = parser.parse_args()

project_base_dir = get_git_root(os.path.dirname(os.path.abspath(__file__))) 
VOLUMES_MNT = '/Volumes/NODE_F767ZI'
MODEL_FOLDER = Path(args.target)

def main():    
    model_path = MODEL_FOLDER
    files = list(model_path.glob("*"))
    binaries = []
    ran = set()
    for file in files:
        if ".bin" in str(file):
            binaries.append(file)
            pass
        
        model = binaries[0]        
        print(f"Going to work on {model}")
        # Copy the model over, and wait for some time for the utility
        # to flash the model over to the board.        
        time.sleep(5.0)
        shutil.copy(model, VOLUMES_MNT)
        time.sleep(5.0)
        
        # Run the binary
        print("Running binary")
        p = subprocess.Popen(['mbed sterm -r'],   
                             stdout=subprocess.PIPE,
                             shell=True)
        
        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                print("Got:", line)
                queue.put(str(line))
            out.close()

        q = Queue()
        t = Thread(target=enqueue_output, args=(p.stdout, q))
        t.daemon = True # thread dies with the program
        t.start()
        
        lines = []
        print("Reading lines")
        t_start = time.time()
        while True:
            if time.time() - t_start >= args.timelimit:
                break
            try:  
                line = q.get(timeout=.1) # or q.get(timeout=.1)
                lines.append(str(line))
                print("Appending line: ", line)
            except:
                continue

        print("Writing lines")
        print(lines)
        with open(args.output_path, "w") as f:
            f.write("".join([x.decode("utf-8") for x in lines]))

        # Hack to only eval 1 binary
        break


if __name__ == '__main__':
    main()
