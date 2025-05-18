# This module creates a TF-IDF table based on the cleaned title and abstract tables.
# It processes the data in chunks to avoid RAM-overload. All data is combined into a single table.
# The SourceFile column is excluded to reduce memory usage.

import pandas as pd                                             # For reading and writing CSV files.
from sklearn.feature_extraction.text import TfidfVectorizer     # For creating the TF-IDF matrix.
from pathlib import Path                                        # For working with file paths.
import csv                                                      # For controlling CSV output quoting.

from variables import (
    csv_folder,
    CUSTOM_DOMAIN_STOPWORDS_TF_IDF,
    title_abstract_max_features,
    title_abstract_ngram_range,
    min_df_profiling,
    max_df_profiling,
    tfidf_chunk_size
)

# Set input and output paths.
csv_folder = Path(csv_folder)
input_path = csv_folder / "articles_title_plus_abstract_lower_case.csv"
output_path_1 = csv_folder / "tfidf_title_plus_abstract_part1.csv"
output_path_2 = csv_folder / "tfidf_title_plus_abstract_part2.csv"
final_output_path = csv_folder / "tfidf_title_plus_abstract.csv"

def main():
    # Load the first chunk of rows to fit the TF-IDF vocabulary.
    part1_df = pd.read_csv(input_path, sep="~", nrows=tfidf_chunk_size)
    part1_df["Title_plus_abstract"] = part1_df["Title_plus_abstract"].fillna("")

    # Fit the TF-IDF vectorizer on the initial chunk.
    vectorizer = TfidfVectorizer(
        max_features=title_abstract_max_features,
        ngram_range=title_abstract_ngram_range,
        stop_words=list(CUSTOM_DOMAIN_STOPWORDS_TF_IDF),
        min_df=min_df_profiling,
        max_df=max_df_profiling
    )
    X_part1 = vectorizer.fit_transform(part1_df["Title_plus_abstract"])

    # Transform TF-IDF for part 1 and place PMID as first column
    features_part1 = pd.DataFrame.sparse.from_spmatrix(
        X_part1, columns=[f"title_abstract__{t}" for t in vectorizer.get_feature_names_out()]
    )
    features_part1.insert(0, "PMID", part1_df["PMID"])  # Ensure PMID is first column
    features_part1.to_csv(output_path_1, sep="~", index=False)
    print(f"Saved: part 1 ({features_part1.shape})")
    features_part1.iloc[0:0].to_csv(output_path_2, sep="~", index=False)

    # Prepare column names for consistent chunked reading.
    column_names = pd.read_csv(input_path, sep="~", nrows=0).columns.tolist()


    # Now that part 1 has been created, the remaining data is processed in chunks and appended.
    print(f"Processing remaining rows in chunks of {tfidf_chunk_size}")
    chunk_generator = pd.read_csv(
        input_path,
        sep="~",
        skiprows=range(1, tfidf_chunk_size + 1),
        header=0,
        chunksize=tfidf_chunk_size
    )

    first_chunk = True
    for chunk in chunk_generator:
        chunk["Title_plus_abstract"] = chunk["Title_plus_abstract"].fillna("")

        # Transform chunk using the fitted vectorizer
        X_chunk = vectorizer.transform(chunk["Title_plus_abstract"])
        df_chunk = pd.DataFrame.sparse.from_spmatrix(
            X_chunk, columns=[f"title_abstract__{t}" for t in vectorizer.get_feature_names_out()]
        )

        # Correctly insert PMID from chunk (from original source!)
        df_chunk.insert(0, "PMID", chunk["PMID"].values)

        df_chunk.to_csv(
            output_path_2,
            sep="~",
            mode="w" if first_chunk else "a",
            index=False,
            header=first_chunk,
            quoting=csv.QUOTE_MINIMAL
        )

        first_chunk = False


    print(f"All chunks saved to: {output_path_2}")

    # Combine both parts into the final TF-IDF output.
    part2_df = pd.read_csv(output_path_2, sep="~")
    combined_df = pd.concat([features_part1, part2_df], axis=0).reset_index(drop=True)

    # Ensure PMID is the first column
    pmid = combined_df.pop("PMID")
    combined_df.insert(0, "PMID", pmid)

    combined_df.to_csv(final_output_path, sep="~", index=False)

    print(f"Combined TF-IDF saved ({combined_df.shape})")

    # Check tfidf_title_plus_abstract_part1.csv
    part1 = pd.read_csv(csv_folder / "tfidf_title_plus_abstract_part1.csv", sep="~", nrows=0)
    print(f"\ntfidf_title_plus_abstract_part1.csv")
    print(f"Columns: {len(part1.columns)}")
    print(f"First column: {part1.columns[0]}")

    # Check tfidf_title_plus_abstract_part2.csv
    part2 = pd.read_csv(csv_folder / "tfidf_title_plus_abstract_part2.csv", sep="~", nrows=0)
    print("\ntfidf_title_plus_abstract_part2.csv")
    print(f"Columns: {len(part2.columns)}")
    print(f"First column: {part2.columns[0]}")

    # Check tfidf_title_plus_abstract.csv
    final = pd.read_csv(csv_folder / "tfidf_title_plus_abstract.csv", sep="~", nrows=0)
    print("\ntfidf_title_plus_abstract.csv")
    print(f"Columns: {len(final.columns)}")
    print(f"First column: {final.columns[0]}")

    # Check if the number of rows matches between input and final TF-IDF file
    input_rows = pd.read_csv(input_path, sep="~").shape[0]
    final_rows = pd.read_csv(csv_folder / "tfidf_title_plus_abstract.csv", sep="~").shape[0]
    print(f"\nInput rows: {input_rows}")
    print(f"TF-IDF output rows: {final_rows}")
if __name__ == "__main__":
    main()
