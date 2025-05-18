# Combine all binary binary data into one feature matrix. For this the following tables are used:
# - articles.csv (containing the PMID and SourceFile);
# - keywords_transformed;
# - mesh_terms_transformed;
# - chemicals_transformed;
# - tfidf_title;
# - tfidf_abstract.

import pandas as pd                      # For loading and merging CSV files
from pathlib import Path                 # For handling file paths

from variables import csv_folder

# Set directory.
csv_folder = Path(csv_folder)
output_path = csv_folder / "data_combined_before_PCA.csv"

def main():
    # Load tables.
    articles = pd.read_csv(csv_folder / "articles.csv", sep="~")
    articles = articles[["PMID", "SourceFile"]] # Include SourceFile again.
    articles["PMID"] = articles["PMID"].astype(str)

    keywords = pd.read_csv(csv_folder / "keywords_transformed.csv", sep="~")
    keywords["PMID"] = keywords["PMID"].astype(str)

    mesh_terms = pd.read_csv(csv_folder / "mesh_terms_transformed.csv", sep="~")
    mesh_terms["PMID"] = mesh_terms["PMID"].astype(str)

    chemicals = pd.read_csv(csv_folder / "chemicals_transformed.csv", sep="~")
    chemicals["PMID"] = chemicals["PMID"].astype(str)

    tfidf_title = pd.read_csv(csv_folder / "tfidf_title.csv", sep="~")
    tfidf_title["PMID"] = tfidf_title["PMID"].astype(str)

    tfidf_abstract = pd.read_csv(csv_folder / "tfidf_abstract.csv", sep="~")
    tfidf_abstract["PMID"] = tfidf_abstract["PMID"].astype(str)

    # Merge all columns using PMID.
    features = articles
    for table in [keywords, mesh_terms, chemicals, tfidf_title, tfidf_abstract]:
        features = features.merge(table, on="PMID", how="left")

    # Replace NaNs with zeros and export combined matrix.
    features = features.fillna(0) # NaN-values cause errors later on.
    features.to_csv(output_path, sep="~", index=False)

    print(f"\nCombined feature matrix created: data_combined_before_PCA.csv, ({features.shape})")

if __name__ == "__main__":
    main()