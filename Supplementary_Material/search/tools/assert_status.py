import json
from glob import glob


dataset_name = "pile"

file_root = f"search/{dataset_name}"
status_files = glob(f"{file_root}/status/*.txt")\

for file in status_files:
    with open(file, 'r') as f:
        assert f.readline().strip() == 'finish'