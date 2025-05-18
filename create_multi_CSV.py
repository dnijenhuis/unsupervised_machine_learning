# This module converts the XML-files to a multi-CSV setup. It sets the columns per CSV. It filters out retracted
# articles, non-2024/2025 articles and articles that do not have an English version.

import os                             # For creating output folder.
import xml.etree.ElementTree as ET    # For parsing XML.
import pandas as pd                   # For working with the CSV files.
from pathlib import Path              # For file system paths.
from tqdm import tqdm                 # Progress bar.

from variables import destination_folder

# Set input and output directories.
destination_folder = Path(destination_folder)
output_dir = destination_folder / "pubmed_csv_export"
os.makedirs(output_dir, exist_ok=True)

def main():
    # Track which files have already been processed.
    processed_files = set()
    articles_path = output_dir / "articles.csv"
    if articles_path.exists():
        try:
            processed_files = set(pd.read_csv(articles_path, sep="~", usecols=["SourceFile"])["SourceFile"].unique())
            print(f"Resuming: {len(processed_files)} files already processed.")
        except Exception as e:
            print("Could not read articles.csv to resume:", e)

    # Create empty CSVs with headers if they don't exist yet. Use '~' symbol since it is much less common than ','. This
    # in order to prevent regular commas in article titles/abstracts from being recognized as column separators.
    def write_headers(filename, columns):
        path = output_dir / filename
        if not path.exists():
            pd.DataFrame(columns=columns).to_csv(path, sep="~", index=False)

    # Determine the CSVs' columns.
    write_headers("articles.csv", ["PMID", "Title", "Abstract", "Year", "SourceFile"])
    write_headers("keywords.csv", ["PMID", "Keyword", "SourceFile"])
    write_headers("mesh_terms.csv", ["PMID", "Descriptor", "SourceFile"])
    write_headers("chemicals.csv", ["PMID", "Chemical", "SourceFile"])

    # Append a DataFrame to a CSV file. An append method was chosen because loading the full
    # dataset at once overload the RAM.
    def append(df, filename):
        df.to_csv(output_dir / filename, mode="a", header=False, sep="~", index=False)

    # The for-loop goes through all PubMed XML files and extracts the relevant data.
    # For each file, the script parses its contents and filters out retracted articles and
    # non 2024/2025 articles.
    # It then extracts data including keywords, MeSH terms, and chemical names.
    # The extracted data is
    # temporarily stored and appended (due to RAM-overload).

    xml_files = sorted(destination_folder.glob("*.xml"))
    for xml_file in tqdm(xml_files, desc="Processing XML files", unit="file"):
        if xml_file.name in processed_files:
            continue

        source_file = xml_file.name # Create source file data to be able to trace back data to origin.
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Temporary storage for rows to write.
        articles, keywords = [], []
        mesh_terms, chemicals = [], []

        for article in root.findall("PubmedArticle"):
            medline = article.find("MedlineCitation")
            article_data = medline.find("Article") if medline is not None else None
            pmid = medline.find("PMID").text if medline is not None else None
            title = article_data.find("ArticleTitle").text if article_data is not None else None

            # Filter out retracted articles.
            is_retracted = any(
                note.attrib.get("RefType", "") == "RetractionIn"
                for note in medline.findall(".//CommentsCorrections")
            )
            if is_retracted:
                continue

            # Extract publication year.
            journal = article_data.find("Journal") if article_data is not None else None
            pub_date = journal.find(".//PubDate") if journal is not None else None
            year = pub_date.find("Year").text if pub_date is not None and pub_date.find("Year") is not None else None

            # Filter out non-2024/2025 years.
            if year not in ["2024", "2025"]:
                continue

            # Filter out articles without at least an English version.
            langs = article_data.findall("Language")
            if not any(lang.text == "eng" for lang in langs if lang is not None):
                continue

            # Extract abstract text.
            abstract = ""
            if article_data is not None:
                abstract_element = article_data.find("Abstract")
                if abstract_element is not None:
                    abstract_texts = abstract_element.findall("AbstractText")
                    abstract = " ".join(
                        "".join(elem.itertext()).strip()
                        for elem in abstract_texts
                        if elem is not None
                    )

            articles.append({
                "PMID": pmid,
                "Title": title,
                "Abstract": abstract,
                "Year": year,
                "SourceFile": source_file
            })

            for keyword in medline.findall(".//Keyword"):
                keywords.append({
                    "PMID": pmid,
                    "Keyword": keyword.text,
                    "SourceFile": source_file
                })

            for mesh in medline.findall(".//MeshHeading"):
                descriptor = mesh.find("DescriptorName")
                mesh_terms.append({
                    "PMID": pmid,
                    "Descriptor": descriptor.text if descriptor is not None else None,
                    "SourceFile": source_file
                })

            for chem in medline.findall(".//Chemical"):
                name = chem.find("NameOfSubstance")
                chemicals.append({
                    "PMID": pmid,
                    "Chemical": name.text if name is not None else None,
                    "SourceFile": source_file
                })

        append(pd.DataFrame(articles), "articles.csv")
        append(pd.DataFrame(keywords), "keywords.csv")
        append(pd.DataFrame(mesh_terms), "mesh_terms.csv")
        append(pd.DataFrame(chemicals), "chemicals.csv")

    # Print statement that multi-CSV setup is complete.
    print("\nMulti-CSV setup complete.")
if __name__ == "__main__":
    main()
