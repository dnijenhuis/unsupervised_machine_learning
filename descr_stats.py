# Generate statistics for the casestudy document. The output of this module is not used further in this pipeline.

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from variables import csv_folder

# Set paths
csv_folder = Path(csv_folder)

def main():
    # Load data
    articles = pd.read_csv(csv_folder / "articles.csv", sep="~")
    keywords = pd.read_csv(csv_folder / "keywords.csv", sep="~")
    mesh_terms = pd.read_csv(csv_folder / "mesh_terms.csv", sep="~")
    chemicals = pd.read_csv(csv_folder / "chemicals.csv", sep="~")

    # Keyword stats
    unique_keywords = keywords["Keyword"].nunique()
    avg_keywords_per_article = keywords.groupby("PMID").size().mean()

    # MeSH term stats
    unique_mesh = mesh_terms["Descriptor"].nunique()
    avg_mesh_per_article = mesh_terms.groupby("PMID").size().mean()

    # Chemical stats
    unique_chem = chemicals["Chemical"].nunique()
    avg_chem_per_article = chemicals.groupby("PMID").size().mean()

    # Additional stats
    missing_pmids = articles["PMID"].isna().sum()

    # Print stats
    print("\n--- PubMed Summary Statistics ---")
    print(f"Unique Keywords: {unique_keywords}")
    print(f"Average Keywords per Article: {avg_keywords_per_article:.2f}")
    print(f"Unique MeSH Terms: {unique_mesh}")
    print(f"Average MeSH Terms per Article: {avg_mesh_per_article:.2f}")
    print(f"Unique Chemicals: {unique_chem}")
    print(f"Average Chemicals per Article: {avg_chem_per_article:.2f}")
    print(f"Articles without PMID: {missing_pmids}")

    # Articles per year.
    print("\nArticles per Year:")
    articles_per_year = articles["Year"].value_counts().sort_index()
    print(articles_per_year)

    # Top 10 most common Keywords, MeSH-terms and Chemicals.
    print("\nTop 10 Keywords:")
    print(keywords["Keyword"].value_counts().head(10))

    print("\nTop 10 MeSH Terms:")
    print(mesh_terms["Descriptor"].value_counts().head(10))

    print("\nTop 10 Chemicals:")
    print(chemicals["Chemical"].value_counts().head(10))
if __name__ == "__main__":
    main()