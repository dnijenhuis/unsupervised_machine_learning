# This module creates 2 separate TF-IDF tables for titles and abstracts based on the cleaned lowercase files.
# The resulting tables are saved as CSVs which include the created features. SourceFile is excluded to reduce RAM-usage.

import pandas as pd                                            # For reading and writing CSV files.
from sklearn.feature_extraction.text import TfidfVectorizer    # For creating TF-IDF tables.
from pathlib import Path                                       # For file system paths.

from variables import (
    csv_folder,
    CUSTOM_DOMAIN_STOPWORDS_TF_IDF,
    title_max_features,
    title_ngram_range,
    abstract_max_features,
    abstract_ngram_range,
    min_df_clustering,
    max_df_clustering
)

# Set directory.
csv_folder = Path(csv_folder)

def main():
    # Fill missing text entries with empty strings.
    def clean_column(df, column_name):
        df[column_name] = df[column_name].fillna("")
        return df

    # Load and process title data.
    title_df = pd.read_csv(csv_folder / "articles_title_lower_case.csv", sep="~")
    title_df = clean_column(title_df, "Title")

    # Create TF-IDF table for title. Use variables as set in variables module.
    tfidf_title = TfidfVectorizer(
        max_features=title_max_features,
        ngram_range=title_ngram_range,
        stop_words=list(CUSTOM_DOMAIN_STOPWORDS_TF_IDF),
        min_df=min_df_clustering,
        max_df=max_df_clustering
    )
    X_title = tfidf_title.fit_transform(title_df["Title"])

    # Store title TF-IDF output.
    title_features = pd.DataFrame.sparse.from_spmatrix(
        X_title, columns=[f"title__{t}" for t in tfidf_title.get_feature_names_out()]
    )
    title_features["PMID"] = title_df["PMID"]
    title_features.to_csv(csv_folder / "tfidf_title.csv", sep="~", index=False)
    print(f"Saved: tfidf_title.csv ({title_features.shape})")

    # Load and process abstract data.
    abstract_df = pd.read_csv(csv_folder / "articles_abstract_lower_case.csv", sep="~")
    abstract_df = clean_column(abstract_df, "Abstract")

    # Create TF-IDF table for abstract. Use variables as set in variables module.
    tfidf_abstract = TfidfVectorizer(
        max_features=abstract_max_features,
        ngram_range=abstract_ngram_range,
        stop_words=list(CUSTOM_DOMAIN_STOPWORDS_TF_IDF),
        min_df=min_df_clustering,
        max_df=max_df_clustering
    )
    X_abstract = tfidf_abstract.fit_transform(abstract_df["Abstract"])

    # Store abstract TF-IDF output.
    abstract_features = pd.DataFrame.sparse.from_spmatrix(
        X_abstract, columns=[f"abstract__{t}" for t in tfidf_abstract.get_feature_names_out()]
    )
    abstract_features["PMID"] = abstract_df["PMID"]
    abstract_features.to_csv(csv_folder / "tfidf_abstract.csv", sep="~", index=False)
    print(f"Saved: tfidf_abstract.csv ({abstract_features.shape})")
if __name__ == "__main__":
    main()