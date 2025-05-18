# This script lowercases and cleans text fields from the created multi-CSV setup.
# As explained in the case study document, the data contains (e.g.) both 'Cancer' and
# 'cancer' keywords.
# The module creates new files for Keywords, MeSH and Chemicals. However, instead of
# creating one lower-case copy for the articles.csv, three separate files are
# created:
# 1. articles_title_lower_case.csv
# 2. articles_abstract_lower_case.csv
# 3. articles_title_and_abstract_lower_case.csv
# File number 3 has newly engineered data. A combination of title and abstract.
# The reason that 3 new files are created, is that these new files will be
# used as input for TF-IDF later on. Each of these TF-IDF executions will result in a separate
# table with data.

import pandas as pd             # For reading and writing CSV files.
import re                       # For cleaning and normalizing text.
from pathlib import Path        # For working with file paths.

from variables import csv_folder

# Set directory containing input CSVs.
csv_folder = Path(csv_folder)

def main():
    # Load CSVs to be processed.
    articles_df = pd.read_csv(csv_folder / "articles.csv", sep="~")
    keywords_df = pd.read_csv(csv_folder / "keywords.csv", sep="~")
    mesh_df = pd.read_csv(csv_folder / "mesh_terms.csv", sep="~")
    chemicals_df = pd.read_csv(csv_folder / "chemicals.csv", sep="~")

    # Clean and normalize text by converting to lowercase, stripping whitespace,
    # and replacing tabs, etc. with a single space.
    def clean_text(text):
        return re.sub(r"\s+", " ", str(text).lower().strip())

    # Create lowercase title file.
    title_df = articles_df[["PMID", "Title", "SourceFile"]].copy()
    title_df["Title"] = title_df["Title"].apply(clean_text)
    title_df.to_csv(csv_folder / "articles_title_lower_case.csv", sep="~", index=False)
    print("Created: articles_title_lower_case.csv")

    # Create lowercase abstract file.
    abstract_df = articles_df[["PMID", "Abstract", "SourceFile"]].copy()
    abstract_df["Abstract"] = abstract_df["Abstract"].apply(clean_text)
    abstract_df.to_csv(csv_folder / "articles_abstract_lower_case.csv", sep="~", index=False)
    print("Created: articles_abstract_lower_case.csv")

    # Create lowercase ('title'+'abstract') file. This is a newly 'engineered' feature.
    combined_df = articles_df[["PMID", "Title", "Abstract", "SourceFile"]].copy()
    combined_df["Title_plus_abstract"] = (
        combined_df["Title"].fillna("") + " " + combined_df["Abstract"].fillna("")
    ).apply(clean_text)
    combined_df = combined_df[["PMID", "Title_plus_abstract"]] # SourceID left out due to RAM-limit later in process.
    combined_df.to_csv(csv_folder / "articles_title_plus_abstract_lower_case.csv", sep="~", index=False)
    print("Created: articles_title_plus_abstract_lower_case.csv")

    # Create lowercase keyword file.
    keywords_df["Keyword"] = keywords_df["Keyword"].apply(clean_text)
    keywords_df.to_csv(csv_folder / "keywords_lower_case.csv", sep="~", index=False)
    print("Created: keywords_lower_case.csv")

    # Create lowercase MeSH-term file.
    mesh_df["Descriptor"] = mesh_df["Descriptor"].apply(clean_text)
    mesh_df.to_csv(csv_folder / "mesh_terms_lower_case.csv", sep="~", index=False)
    print("Created: mesh_terms_lower_case.csv")

    # Create lowercase Chemical file.
    chemicals_df["Chemical"] = chemicals_df["Chemical"].apply(clean_text)
    chemicals_df.to_csv(csv_folder / "chemicals_lower_case.csv", sep="~", index=False)
    print("Created: chemicals_lower_case.csv")

if __name__ == "__main__":
    main()