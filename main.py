# This is the main module for the unsupervised machine learning solution. Its only function is to execute the whole
# pipeline from downloading the data to profiling the clusters. Though the code should run automatically from start
# to end, there are charts presented to the user twice. The user should check the charts and close them. After this,
# the user needs to provide input. Specifically:
# 1. The number of PCA-components (based on the (cumulative) explained variance per component graph);
# 2. The number of clusters (based on various quality metrics graphs).
import variables # Import variables necessary for other modules.
import retrieve_data # Download PubMed data and MD5-files.
import check_hashes_gz_files # Verify MD5 hashes of downloaded files.
import create_multi_CSV # Convert XML files into multi-CSV setup..
import data_checking # Validate and CSV files.
import descr_stats # Present descriptive statistics for case study. This output is not used further in this pipeline.
import convert_to_lower_case # Convert text fields to lowercase and strip unneccessary spaces.
import transform_categorical_to_binary # Encode the cleaned Keywords, MeSH-terms, and Chemicals.
import perform_tf_idf_on_title_and_abstract # Create TF-IDF features for title and abstract.
import perform_tf_idf_on_title_plus_abstract # Create TF-IDF features for ('title' + 'abstract').
import combine_transformed_data # Merge all features into one matrix.
import perform_PCA # Apply standardization and PCA.
import clustering # Run K-means clustering.
import profiling_clusters # Generate profiles for each cluster.

def main():
    # This function executes the whole pipeline from downloading files to creating and profiling clusters.
    retrieve_data.main()
    check_hashes_gz_files.main()
    create_multi_CSV.main()
    data_checking.main()
    descr_stats.main()
    convert_to_lower_case.main()
    transform_categorical_to_binary.main()
    perform_tf_idf_on_title_and_abstract.main()
    perform_tf_idf_on_title_plus_abstract.main()
    combine_transformed_data.main()
    perform_PCA.main()
    clustering.main()
    profiling_clusters.main()

if __name__ == "__main__":
    main()
