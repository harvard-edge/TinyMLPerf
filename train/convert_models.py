"""Convert models from .pb serialized TF format to actual C++ files that can
be used in our MCUs. Will try to convert and output these model files to the
same directory as where the .pb files were originally, to make it easy to
test."""
from subprocess import run
from pathlib import Path
import time


def main():
    model_path = Path.cwd() / 'models'
    folders = list(model_path.glob("*"))
    for folder in folders:
        models = list(folder.glob('*.pb'))
        if not models:
            continue
        
        model_name = models[0]
        run(['utensor-cli', 'convert',
            str(model_name), '--output-nodes', 'pred', 
            '--model-dir', folder])


if __name__ == '__main__':
    main()
