"""Quick script to do some grid searching when training models."""
import numpy as np
from subprocess import run
from pathlib import Path

def main():
    model_dir = Path.cwd() / 'models'
    model_dir.mkdir(exist_ok=True, parents=True)
    
    # for network in ['fc1', 'fc2', 'fc3', '1', '2']:
    #     output_folder = model_dir / network
    #     output_folder.mkdir(exist_ok=True, parents=True)
    #     output_path = output_folder / 'model.pb'
    #     run([
    #         'python', 'train.py',
    #         '--output-pb', str(output_path),
    #         '--epochs', '1',
    #         '--graph', network,
    #     ])
    
    # for network in ['fc1', 'fc2', 'fc3']:
    #     output_folder = model_dir / network
    #     output_folder.mkdir(exist_ok=True, parents=True)
    #     run([
    #         'python', 'deep_mlp.py',
    #         '--output-dir', str(output_folder),
    #         '--output', 'model.pb',
    #         '--model', network,
    #     ])

    for first_layer in [32, 48, 64, 92, 128, 256, 384, 512]:
        for second_layer in [32, 48, 64, 92, 128, 256, 384, 512]:
            if first_layer < second_layer:
                continue
            output_folder = model_dir / "twolayer_{}_{}".format(first_layer, second_layer)
            output_folder.mkdir(exist_ok=True, parents=True)
            run([
                'python', 'deep_mlp.py',
                '--output-dir', str(output_folder),
                '--output', 'model.pb',
                '--first-layer', str(first_layer),
                '--second-layer', str(second_layer),
            ])




if __name__ == '__main__':
    main()