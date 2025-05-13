from huggingface_hub import snapshot_download, login, list_repo_files
import os
import time
import traceback


datasets = ['bigscience-data/roots_en_the_pile_uspto', 'bigscience-data/roots_en_wiktionary', 'bigscience-data/roots_en_wikipedia', 'bigscience-data/roots_en_wikivoyage', 'bigscience-data/roots_en_wikiquote', 'bigscience-data/roots_en_wikibooks', 'bigscience-data/roots_en_wikiversity', 'bigscience-data/roots_en_wikinews', 'bigscience-data/roots_en_royal_society_corpus', 'bigscience-data/roots_en_ted_talks_iwslt', 'bigscience-data/roots_en_the_pile_europarl', 'bigscience-data/roots_en_no_code_stackexchange', 'bigscience-data/roots_en_book_dash_books', 'bigscience-data/roots_en_odiencorp', 'bigscience-data/roots_en_uncorpus']

for dataset in datasets:
    while True:
        time.sleep(0.2)
        try:
            login(token='', add_to_git_credential=True)
            snapshot_download(repo_id=dataset,
                                        repo_type="dataset",
                                        local_dir=f"datasets/{dataset.split('/')[-1].replace('roots_en_', 'roots_en/')}",
                                        local_dir_use_symlinks=True,
                                        etag_timeout=60,
                                        max_workers=1)
        except:
            traceback.print_exc()
            continue
        print(f"{dataset} done")
        break