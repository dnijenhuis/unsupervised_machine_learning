# This module clusters the data using the selected number of principal components. Specifically, it uses K-Means.

import pandas as pd                                      # For loading and saving data.
from sklearn.cluster import KMeans                       # For clustering.
from sklearn.metrics import silhouette_score             # For cluster quality evaluation.
import matplotlib.pyplot as plt                          # For plotting metrics.
import matplotlib.ticker as ticker                       # Idem.
import numpy as np                                       # For BIC approximation.
from pathlib import Path                                 # For handling file paths.
from variables import csv_folder                         # Path to final output folder.

# Set directories.
csv_folder_path = Path(csv_folder)
input_path = csv_folder_path / "data_after_pca.csv"
output_path = csv_folder_path / "data_with_clusters.csv"

def main():
    # Load data.
    df = pd.read_csv(input_path, sep="~")
    X = df[[c for c in df.columns if c.startswith("pca_")]]

    # Evaluate clustering metrics.
    k_range = range(2, 20)
    X_sample = X.sample(n=65000, random_state=20250501)

    inertias = []
    silhouette_scores = []
    bic_scores = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=20250501, n_init="auto")
        labels = model.fit_predict(X_sample)

        inertias.append(model.inertia_)
        silhouette_scores.append(silhouette_score(X_sample, labels))

        n, d = X_sample.shape
        bic = n * np.log(model.inertia_ / n) + k * d * np.log(n)
        bic_scores.append(bic)

    # Plot evaluation metrics.
    plt.figure(figsize=(15, 4))

    plt.subplot(1, 3, 1)
    plt.plot(k_range, inertias, marker="o")
    plt.title("Elbow Method")
    plt.xlabel("K")
    plt.ylabel("Inertia")
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.subplot(1, 3, 2)
    plt.plot(k_range, silhouette_scores, marker="o", color="green")
    plt.title("Silhouette Score")
    plt.xlabel("K")
    plt.ylabel("Score")
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.subplot(1, 3, 3)
    plt.plot(k_range, bic_scores, marker="o", color="purple")
    plt.title("BIC Score")
    plt.xlabel("K")
    plt.ylabel("BIC")
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    plt.tight_layout()
    plt.show()

    # Ask input from user: number of clusters.
    chosen_k = int(input("User input required. Enter the number of clusters (K): "))

    # Fit final KMeans model.
    final_model = KMeans(n_clusters=chosen_k, random_state=20250501, n_init="auto")
    df["Cluster"] = final_model.fit_predict(X) + 1  # Start counting clusters at 1, not at 0.

    # Save output.
    df.to_csv(output_path, sep="~", index=False)
    print(f"Saved: data_with_clusters ({df.shape})")

    # Final checks: compare row counts and PMIDs in clustered output vs original articles.csv.
    clusters_df = pd.read_csv(output_path, sep="~")
    articles_df = pd.read_csv(csv_folder_path / "articles.csv", sep="~")

    print(f"Rows in clustered output: {len(clusters_df)}")
    print(f"Rows in articles.csv: {len(articles_df)}")

    missing_pmid_count = clusters_df["PMID"].isnull().sum()
    print(f"Rows with missing PMID in clustered output: {missing_pmid_count}")

    duplicate_pmid_count = clusters_df["PMID"].duplicated().sum()
    print(f"Duplicate PMIDs in clustered output: {duplicate_pmid_count}")

    clusters_pmids = set(clusters_df["PMID"].astype(str))
    article_pmids = set(articles_df["PMID"].astype(str))
    print(f"All cluster member PMIDs are in articles.csv: {clusters_pmids.issubset(article_pmids)}")
    print(f"All articles.csv article PMIDs are in clustered output: {article_pmids.issubset(clusters_pmids)}")

    # Plot clusters using first four PCA components.
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    for cluster_id in sorted(df["Cluster"].unique()):
        cluster_points = df[df["Cluster"] == cluster_id]
        plt.scatter(cluster_points["pca_1"], cluster_points["pca_2"], label=f"Cluster {cluster_id}", s=10)
    plt.title("Clusters: PCA 1 vs 2")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
 #   plt.legend(markerscale=2, fontsize="small")

    plt.subplot(1, 2, 2)
    for cluster_id in sorted(df["Cluster"].unique()):
        cluster_points = df[df["Cluster"] == cluster_id]
        plt.scatter(cluster_points["pca_2"], cluster_points["pca_3"], label=f"Cluster {cluster_id}", s=10)
    plt.title("Clusters: PCA 2 vs 3")
    plt.xlabel("PCA 3")
    plt.ylabel("PCA 4")
 #   plt.legend(markerscale=2, fontsize="small")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
