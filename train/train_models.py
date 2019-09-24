"""Quick script to do some grid searching when training models."""
import numpy as np
from subprocess import run
from pathlib import Path

def main():
    model_dir = Path.cwd() / 'models'
    model_dir.mkdir(exist_ok=True, parents=True)
    
    for network in ['fc1', '1', '2']:
        output_folder = model_dir / network
        output_folder.mkdir(exist_ok=True, parents=True)
        output_path = output_folder / 'model.pb'
        run([
            'python', 'train.py',
            '--output-pb', str(output_path),
            '--epochs', '1',
            '--graph', network,
        ])


if __name__ == '__main__':
    main()