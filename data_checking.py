# This script validates the structure and content of the created CSV-files. It checks the
# number of columns per CSV, the PubMedID format and uniqueness, and whether the parent
# and child tables are have relations (every child has a parent). It is also checks if every
# article is from 2024/2025.

import pandas as pd             # For reading and inspecting CSV files.
from pathlib import Path        # For working with file paths.
from tqdm import tqdm           # Progress bar.

from variables import destination_folder, csv_folder

destination_folder = Path(destination_folder)
csv_folder = Path(csv_folder)

def main():
    # Check number of columns in articles.csv.
    articles_df = pd.read_csv(csv_folder / "articles.csv", sep="~")
    if articles_df.shape[1] == 5:
        print("Column count for articles.csv is correct (5)")
    else:
        print(f"Incorrect column count in articles.csv: found {articles_df.shape[1]}, expected 5")

    # Check number of columns in chemicals.csv.
    chemicals_df = pd.read_csv(csv_folder / "chemicals.csv", sep="~")
    if chemicals_df.shape[1] == 3:
        print("Column count for chemicals.csv is correct (3)")
    else:
        print(f"Incorrect column count in chemicals.csv: found {chemicals_df.shape[1]}, expected 3")

    # Check number of columns in keywords.csv.
    keywords_df = pd.read_csv(csv_folder / "keywords.csv", sep="~")
    if keywords_df.shape[1] == 3:
        print("Column count for keywords.csv is correct (3)")
    else:
        print(f"Incorrect column count in keywords.csv: found {keywords_df.shape[1]}, expected 3")

    # Check number of columns in mesh_terms.csv.
    mesh_df = pd.read_csv(csv_folder / "mesh_terms.csv", sep="~")
    if mesh_df.shape[1] == 3:
        print("Column count for mesh_terms.csv is correct (3)")
    else:
        print(f"Incorrect column count in mesh_terms.csv: found {mesh_df.shape[1]}, expected 3")

    # Check that all PMIDs are numeric.
    non_numeric_pmids = articles_df[~articles_df["PMID"].astype(str).str.isdigit()]
    if non_numeric_pmids.empty:
        print("All PMIDs in articles.csv are numeric")
    else:
        print(f"\n{len(non_numeric_pmids)} invalid PMIDs (non-numeric) found in articles.csv")

    # Check for PMID duplicates.
    duplicates = articles_df["PMID"].astype(str).duplicated().sum()
    if duplicates:
        print(f"{duplicates} duplicate PMIDs found in articles.csv")
    else:
        print("No duplicate PMIDs found in articles.csv")

    # Check that all PMIDs in chemicals.csv exist in articles.csv, so every child has a parent.
    pmids_in_articles = set(articles_df["PMID"].astype(str))
    chemicals_df = pd.read_csv(csv_folder / "chemicals.csv", sep="~")
    chemicals_pmids = set(chemicals_df["PMID"].astype(str))
    unmatched_chemicals = chemicals_pmids - pmids_in_articles
    if unmatched_chemicals:
        print(f"{len(unmatched_chemicals)} PMIDs in chemicals.csv are not found in articles.csv")
    else:
        print("All PMIDs in chemicals.csv are matched in articles.csv")

    # Check that all PMIDs in keywords.csv exist in articles.csv, so every child has a parent.
    keywords_df = pd.read_csv(csv_folder / "keywords.csv", sep="~")
    keywords_pmids = set(keywords_df["PMID"].astype(str))
    unmatched_keywords = keywords_pmids - pmids_in_articles
    if unmatched_keywords:
        print(f"{len(unmatched_keywords)} PMIDs in keywords.csv are not found in articles.csv")
    else:
        print("All PMIDs in keywords.csv are matched in articles.csv")

    # Check that all PMIDs in mesh_terms.csv exist in articles.csv, so every child has a parent.
    mesh_df = pd.read_csv(csv_folder / "mesh_terms.csv", sep="~")
    mesh_pmids = set(mesh_df["PMID"].astype(str))
    unmatched_mesh = mesh_pmids - pmids_in_articles
    if unmatched_mesh:
        print(f"{len(unmatched_mesh)} PMIDs in mesh_terms.csv are not found in articles.csv")
    else:
        print("All PMIDs in mesh_terms.csv are matched in articles.csv")

    # Check that all Year values are 2024 or 2025.
    invalid_years = articles_df[~articles_df["Year"].astype(str).isin(["2024", "2025"])]
    if invalid_years.empty:
        print("All articles are 2024 or 2025 publications")
    else:
        print(f"{len(invalid_years)} articles are not from 2024 or 2025")

    print("\nData check complete.")
if __name__ == "__main__":
    main()
