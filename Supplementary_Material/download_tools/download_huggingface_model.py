from huggingface_hub import snapshot_download, login
import time
import traceback
import pandas as pd


models = ['bigscience/bloom']

for model in models:
    while True:
        time.sleep(0.2)
        try:
            login(token='', add_to_git_credential=True)
            snapshot_download(repo_id=f"{model}",
                                        repo_type="model",
                                        ignore_patterns=["flax_model*", "model.fp32*", "tf_model*", "rust_model*", "onnx*", "*.bin", "tensorboard*"],
                                        local_dir=f"models/{model.split('/')[-1]}",
                                        local_dir_use_symlinks=True,
                                        etag_timeout=60,
                                        max_workers=1)
        except:
            traceback.print_exc()
            continue
        print(f"{model} done")
        break