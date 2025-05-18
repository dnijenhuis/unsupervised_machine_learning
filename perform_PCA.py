# Apply PCA to the combined feature matrix consisting of Keywords, MeSH-terms Chemicals, and
# TF-IDF data created based on titles and abstracts. Because of RAM-overlad this is done in chunks.

import pandas as pd
import numpy as np
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from pathlib import Path
from variables import csv_folder

# Set directories.
csv_folder = Path(csv_folder)
input_path = csv_folder / "data_combined_before_PCA.csv"
output_path = csv_folder / "data_after_pca.csv"

def main():
    # Chunk size.
    chunk_size = 100000

    # Load metadata separately.
    meta_df = pd.read_csv(input_path, sep="~", usecols=["PMID", "SourceFile"])

    # First chunk for column names and plotting.
    first_chunk = pd.read_csv(input_path, sep="~", nrows=chunk_size)
    columns_to_drop = ["PMID", "SourceFile"]
    feature_cols = [col for col in first_chunk.columns if col not in columns_to_drop]

    # Prepare scaler and PCA
    scaler = StandardScaler()
    ipca = IncrementalPCA()

    # First pass: fit scaler and PCA incrementally
    reader = pd.read_csv(input_path, sep="~", chunksize=chunk_size)
    for i, chunk in enumerate(reader):
        data = chunk[feature_cols]
        scaled = scaler.partial_fit(data) if i == 0 else scaler.partial_fit(data)

    reader = pd.read_csv(input_path, sep="~", chunksize=chunk_size)
    for chunk in reader:
        scaled_chunk = scaler.transform(chunk[feature_cols])
        ipca.partial_fit(scaled_chunk)

    # Extract explained variance
    explained = ipca.explained_variance_ratio_
    cumulative = np.cumsum(explained)

    # Plot explained and cumulative variance
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(explained) + 1), explained, marker="o")
    plt.title("Explained Variance per Component")
    plt.xlabel("Component")
    plt.ylabel("Variance")

    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(cumulative) + 1), cumulative, marker="o")
    plt.title("Cumulative Explained Variance")
    plt.xlabel("Components")
    plt.ylabel("Cumulative Variance")
    plt.tight_layout()
    plt.show()

    # Prompt user for component count
    chosen = int(input("Input required. Enter number of components to keep: "))

    # Fit final IncrementalPCA with chosen components
    ipca_final = IncrementalPCA(n_components=chosen)
    reader = pd.read_csv(input_path, sep="~", chunksize=chunk_size)
    pca_results = []

    for chunk in reader:
        scaled_chunk = scaler.transform(chunk[feature_cols])
        reduced = ipca_final.partial_fit(scaled_chunk)

    reader = pd.read_csv(input_path, sep="~", chunksize=chunk_size)
    for chunk in reader:
        scaled_chunk = scaler.transform(chunk[feature_cols])
        reduced = ipca_final.transform(scaled_chunk)
        pca_results.append(pd.DataFrame(reduced, columns=[f"pca_{i + 1}" for i in range(chosen)]))

    # Combine all PCA chunks and metadata
    pca_df = pd.concat(pca_results, axis=0).reset_index(drop=True)
    meta_df = meta_df.reset_index(drop=True)
    pca_df.insert(0, "SourceFile", meta_df["SourceFile"])
    pca_df.insert(0, "PMID", meta_df["PMID"])

    pca_df.to_csv(output_path, sep="~", index=False)
    print(f"Saved: data_after_pca ({pca_df.shape})")
if __name__ == "__main__":
    main()