from huggingface_hub import snapshot_download, login, list_repo_files
import os
import time
import traceback


datasets = ['monology/pile-uncopyrighted']

for dataset in datasets:
    while True:
        time.sleep(0.2)
        try:
            login(token='', add_to_git_credential=True)
            snapshot_download(repo_id=dataset,
                                        repo_type="dataset",
                                        local_dir=f"datasets/{dataset.split('/')[-1]}",
                                        local_dir_use_symlinks=True,
                                        etag_timeout=60,
                                        max_workers=1)
        except:
            traceback.print_exc()
            continue
        print(f"{dataset} done")
        break