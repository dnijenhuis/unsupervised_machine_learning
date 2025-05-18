# This script applies multi-hot encoding to the cleaned Keywords, MeSH-terms, and Chemical files.
# It creates CSV-files containing the top-N most frequent values for each category.

import pandas as pd             # For reading and writing CSV files.
from pathlib import Path        # For working with file paths.

import variables

# Set directory.
csv_folder = Path(variables.csv_folder)

def main():
    # Convert a categorical column into a multi-hot encoded feature set.
    def multi_hot_encode(filepath, column, top_n, output_name):
        df = pd.read_csv(filepath, sep="~")

        # Keep only the top-N most frequent values.
        top_values = df[column].value_counts().nlargest(top_n).index
        filtered = df[df[column].isin(top_values)]

        # Apply one-hot encoding.
        one_hot = pd.get_dummies(filtered[column])
        result = pd.concat([filtered[["PMID"]], one_hot], axis=1)
        result = result.groupby("PMID").sum().reset_index()

        # Export the result.
        result.to_csv(csv_folder / f"{output_name}_transformed.csv", sep="~", index=False)
        return result

    # Process and export multi-hot encoded features.
    multi_hot_encode(csv_folder / "keywords_lower_case.csv", "Keyword", top_n=variables.top_n_keywords, output_name="keywords")
    multi_hot_encode(csv_folder / "mesh_terms_lower_case.csv", "Descriptor", top_n=variables.top_n_mesh, output_name="mesh_terms")
    multi_hot_encode(csv_folder / "chemicals_lower_case.csv", "Chemical", top_n=variables.top_n_chemicals, output_name="chemicals")

    print("Transformed Keywords, MeSH-terms, and Chemicals to binary format.")
if __name__ == "__main__":
    main()