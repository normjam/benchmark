import os

import wget

# Pull datasets
datasets = {"PBMC3K": "https://ndownloader.figshare.com/files/18789473?private_link=6e12f5f56bb46842f5ee",
            "CITE-seq-bone-marrow": "https://ndownloader.figshare.com/files/18788633?private_link=cfbc86f6a399343677ea",
            "Endoderm-full": "https://ndownloader.figshare.com/files/18789569?private_link=fe99143697ea99121240",
            "Endoderm-downsample": "https://ndownloader.figshare.com/files/18788645?private_link=c204122a8d0550282502"}

for dataset_name, dataset_url in datasets.items():
    print(f"Downloading dataset {dataset_name}")
    wget.download(dataset_url, dataset_name)

# Run datasets on existing methods


def clean_up():
    for dataset_name in datasets:
        print(f"\nDeleting dataset {dataset_name}")
        os.remove(dataset_name)
