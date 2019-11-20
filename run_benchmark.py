from normbench.methods import LogNormalizationRunner, GLMPCAMethodRunner, data, ScViMethodRunner, ScTransformMethodRunner

VERBOSE = False

# Pull datasets
datasets = {
    "pbmc3k": data.pbmc3k(),
    "cite_seq_bone_marrow": data.cite_seq_bone_marrow(),
    "endoderm_downsampled": data.endoderm_downsampled(),
    "endoderm_full": data.endoderm_full()
}

# Run datasets on existing methods
for data_name, data in datasets:
    print(f"Running scVI on dataset {data_name}")
    ScViMethodRunner(data, VERBOSE).run()

    print(f"Running scTransform on dataset {data_name}")
    ScTransformMethodRunner(data, VERBOSE).run()

    print(f"Running LogNorm on dataset {data_name}")
    LogNormalizationRunner(data, VERBOSE).run()

    print(f"Running GLMPCA (Poisson) on dataset {data_name}")
    GLMPCAMethodRunner(data, VERBOSE).run()

    print(f"Running GLMPCA (Negative Binomial) on dataset {data_name}")
    GLMPCAMethodRunner(data, VERBOSE, likelihood="nb").run()
