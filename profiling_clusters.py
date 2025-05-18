# Generate profile CSVs and bar charts for each cluster.

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from variables import (
    csv_folder,
    CUSTOM_DOMAIN_STOPWORDS_PROFILING,
    profiling_number_of_top_keywords,
    profiling_number_of_top_mesh,
    profiling_number_of_top_chemicals,
    profiling_number_of_top_words_in_title_abstract,
    TERM_REPLACEMENTS
)

# Set paths
csv_folder = Path(csv_folder)
output_dir = csv_folder / "cluster_profiles"
output_dir.mkdir(exist_ok=True)

# Replace terms with normalized equivalents
def normalize_term(text):
    text = str(text).strip().lower()
    for original, replacement in TERM_REPLACEMENTS.items():
        text = text.replace(original, replacement)
    return text

def main():
    # Load CSVs
    clusters = pd.read_csv(csv_folder / "data_with_clusters.csv", sep="~")
    keywords = pd.read_csv(csv_folder / "keywords_lower_case.csv", sep="~")
    mesh_terms = pd.read_csv(csv_folder / "mesh_terms_lower_case.csv", sep="~")
    chemicals = pd.read_csv(csv_folder / "chemicals_lower_case.csv", sep="~")
    tfidf = pd.read_csv(csv_folder / "tfidf_title_plus_abstract.csv", sep="~", low_memory=False)

    # Ensure consistent PMIDs.
    for df in [clusters, keywords, mesh_terms, chemicals, tfidf]:
        df["PMID"] = df["PMID"].astype(str)

    # Normalize terms.
    keywords["Keyword"] = keywords["Keyword"].apply(normalize_term)
    mesh_terms["Descriptor"] = mesh_terms["Descriptor"].apply(normalize_term)
    chemicals["Chemical"] = chemicals["Chemical"].apply(normalize_term)

    # Merge cluster labels.
    keywords = keywords.merge(clusters[["PMID", "Cluster"]], on="PMID")
    mesh_terms = mesh_terms.merge(clusters[["PMID", "Cluster"]], on="PMID")
    chemicals = chemicals.merge(clusters[["PMID", "Cluster"]], on="PMID")
    tfidf = tfidf.merge(clusters[["PMID", "Cluster"]], on="PMID")

    # Profile each cluster.
    for cluster_id in sorted(clusters["Cluster"].unique()):
        cluster_data = {}
        cluster_size = clusters["Cluster"].value_counts()[cluster_id]

        # Keywords (relative frequency).
        cluster_keywords = keywords[keywords["Cluster"] == cluster_id]["Keyword"]
        top_keywords = (
            cluster_keywords.value_counts(normalize=False) / cluster_size
        ).drop(labels=CUSTOM_DOMAIN_STOPWORDS_PROFILING, errors="ignore").head(profiling_number_of_top_keywords)
        cluster_data["Top Keywords"] = top_keywords

        # MeSH terms (relative frequency).
        cluster_mesh = mesh_terms[mesh_terms["Cluster"] == cluster_id]["Descriptor"]
        top_mesh = (
            cluster_mesh.value_counts(normalize=False) / cluster_size
        ).drop(labels=CUSTOM_DOMAIN_STOPWORDS_PROFILING, errors="ignore").head(profiling_number_of_top_mesh)
        cluster_data["Top MeSH Terms"] = top_mesh

        # Chemicals (relative frequency).
        cluster_chemicals = chemicals[chemicals["Cluster"] == cluster_id]["Chemical"]
        top_chem = (
            cluster_chemicals.value_counts(normalize=False) / cluster_size
        ).drop(labels=CUSTOM_DOMAIN_STOPWORDS_PROFILING, errors="ignore").head(profiling_number_of_top_chemicals)
        cluster_data["Top Chemicals"] = top_chem

        # TF-IDF: normalize column names, group duplicates, and average.
        tfidf_cols = [col for col in tfidf.columns if col.startswith("title_abstract__")]
        tfidf_cluster = tfidf[tfidf["Cluster"] == cluster_id][tfidf_cols]

        normalized_cols = [
            f"title_abstract__{normalize_term(col.replace('title_abstract__', ''))}" for col in tfidf_cols
        ]
        tfidf_cluster.columns = normalized_cols
        tfidf_cluster = tfidf_cluster.T.groupby(level=0).mean().T

        top_words = tfidf_cluster.mean().sort_values(ascending=False)
        prefixed_stopwords = {f"title_abstract__{w}" for w in CUSTOM_DOMAIN_STOPWORDS_PROFILING}
        top_words = top_words[~top_words.index.isin(prefixed_stopwords)].head(
            profiling_number_of_top_words_in_title_abstract
        )
        cluster_data["Top TF-IDF Title & Abstract Words"] = top_words

        # Remove duplicate index entries.
        for key in cluster_data:
            cluster_data[key] = cluster_data[key][~cluster_data[key].index.duplicated(keep="first")]

        # Save profile CSV.
        profile_df = pd.concat(cluster_data.values(), axis=1)
        profile_df.columns = cluster_data.keys()
        profile_df.to_csv(output_dir / f"cluster_{cluster_id}_profile.csv", sep="~")

        # Plot bar charts.
        fig, axes = plt.subplots(2, 2, figsize=(12, 7))
        axes = axes.flatten()

        for i, (name, series) in enumerate(cluster_data.items()):
            ax = axes[i]
            if not series.empty:
                clean_series = series.copy()
                if "TF-IDF" in name:
                    clean_series.index = clean_series.index.str.replace("title_abstract__", "", regex=False)
                    ax.set_xlabel("Mean TF-IDF Score")
                else:
                    ax.set_xlabel("Frequency / Cluster Size")

                clean_series.sort_values().plot(kind="barh", ax=ax)
                ax.set_title(name)
                ax.set_ylabel("")
            else:
                ax.set_visible(False)

        plt.suptitle(f"Cluster {cluster_id} – Combined Profile", fontsize=22)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(output_dir / f"cluster_{cluster_id}_combined.png")
        plt.close()

    print("\nSaved: cluster profiles (CSV and PNG).")

if __name__ == "__main__":
    main()
