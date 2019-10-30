"""Gets the path to the compiled programs, and automatically runs these on
the MCUs."""
from subprocess import PIPE, Popen
from threading  import Thread
from queue import Queue
import json
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
from power import power

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

def gather_power_metrics():
    # Assumes binary has been flashed to board
    return power()    

def run_on_mcu(model_path):
    files = list(model_path.glob("*.bin"))
    binaries = []
    for file in files:
        if ".bin" in str(file):
            binaries.append(file)
            pass
        
        model = binaries[0]        
        print("Going to work on {}".format(model))

        # Copy the model over, and wait for some time for the utility
        # to flash the model over to the board.  
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
       
        out = None
        lines = []
        t = time.time()
        while True:
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
            print("%f seconds left" % (args.timelimit-(time.time()-t)))
            if time.time()-t >= args.timelimit:
                break
        
        time.sleep(0.5)
        a.kill()
        time.sleep(0.5)
        a.kill()
        
        lines = [x for x in lines if x.decode("utf-8").strip() != ""]
        lines_stacked = "".join([x.decode("utf-8") for x in lines]).strip()
        retval = json.loads(lines_stacked.splitlines()[-1])

        # Run power management
        power_metrics = gather_power_metrics()

        retval.update(power_metrics)
        
        return retval

def main():    
    model_path = MODEL_FOLDER
    for i in range(10):
        try:
            result = run_on_mcu(model_path)
            print("Success!")
            break
        except Exception as e:
            print("Run on mcu failed... Retrying")
            print(e)
            result = {"Error" : "Failed."}
    with open(args.output_path, "w") as f:
        f.write(json.dumps(result))

if __name__ == '__main__':
    main()
