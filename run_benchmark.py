import os

import wget

from methods import LogNormalizationRunner, GLMPCAMethodRunner

VERBOSE = False

# Pull datasets
datasets = {"PBMC3K": "https://ndownloader.figshare.com/files/18789473?private_link=6e12f5f56bb46842f5ee",
            "CITE-seq-bone-marrow": "https://ndownloader.figshare.com/files/18788633?private_link=cfbc86f6a399343677ea",
            "Endoderm-full": "https://ndownloader.figshare.com/files/18789569?private_link=fe99143697ea99121240",
            "Endoderm-downsample": "https://ndownloader.figshare.com/files/18788645?private_link=c204122a8d0550282502"}

for dataset_name, dataset_url in datasets.items():
    if not os.path.exists(dataset_name):
        print(f"\nDownloading dataset {dataset_name}")
        wget.download(dataset_url, dataset_name)

# Run datasets on existing methods
for dataset_name in datasets:
    file_pointer = open(dataset_name, 'rb')
    print(f"Running LogNorm on dataset {dataset_name}")
    LogNormalizationRunner(file_pointer, VERBOSE).run()
    print(f"Running GLMPCA on dataset {dataset_name}")
    GLMPCAMethodRunner(file_pointer, VERBOSE).run()


def clean_up():
    """
    Clean up method that deletes all the downloaded raw datasets.
    """
    for dataset_name in datasets:
        print(f"\nDeleting dataset {dataset_name}")
        os.remove(dataset_name)
