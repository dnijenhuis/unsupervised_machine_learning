# **README**

## **Project Overview**

This repository contains a case study developed for the IU course *Machine Learning – Unsupervised Learning and Feature Engineering*. 
It applies unsupervised machine learning techniques to a large collection of PubMed articles to automatically 
identify current trends in medical science. The input of this pipeline is zipped PubMed data containing XML-files with
article data. The output of this pipeline consists of simple descriptive statistics, and graphs which represent the
various clusters. 

## **Specific unsupervised ML-techniques used**
* Multi-hot encoding;
* TF-IDF;
* Normalization of data;
* Principal Component Analysis (PCA);
* K-Means clustering;
* Cluster profiling.

## **Installation and usage**

To install and run the project, follow these steps:

1. Download all Python files from this repository.
2. Open the project through an IDE (e.g. PyCharm) and set the interpreter. 
3. Make sure you have the required libraries installed. I refer to the case study document for a list of the libraries.
4. Open the `variables.py` file and replace all PLACEHOLDER values with the correct paths.
5. Optionally, adjust variables in `variables.py` to suit your system limits and goals (e.g. maximum features, number of clusters, stopwords).
6. Run `main.py` to execute the full pipeline.
7. During the execution, the user needs to provide input twice based on presented graphs. Specifically:
   * The number of PCA-components (based on the (cumulative) explained variance per component graph);
   * The number of clusters (based on various quality metrics graphs).


## **Description per module**
* `variables.py`: Import variables necessary for other modules.  
* `retrieve_data.py`: Download PubMed data and MD5-files.  
* `check_hashes_gz_files.py`: Verify MD5 hashes of downloaded files.  
* `create_multi_CSV.py`: Convert XML files into multi-CSV setup.  
* `data_checking.py`: Validate and CSV files.  
* `descr_stats.py`: Present descriptive statistics for case study. This output is not used further in this pipeline.  
* `convert_to_lower_case.py`: Convert text fields to lowercase and strip unneccessary spaces.  
* `transform_categorical_to_binary.py`: Encode the cleaned Keywords, MeSH-terms, and Chemicals.  
* `perform_tf_idf_on_title_and_abstract.py`: Create TF-IDF features for title and abstract.  
* `perform_tf_idf_on_title_plus_abstract.py`: Create TF-IDF features for ('title' + 'abstract').  
* `combine_transformed_data.py`: Merge all features into one matrix.  
* `perform_PCA.py`: Apply standardization and PCA.  
* `clustering.py`: Run K-means clustering.  
* `profiling_clusters.py`: Generate profiles for each cluster.

## **Limitations / future development**

* Due to hardware constraints, only a subset of the full dataset was used for TF-IDF fitting. The full pipeline should be executed again with better RAM/hardware. 
* The code could be expanded with a GUI, increasing accessability for users;
* The code could be adjusted so that the various checks and prints in the console during the execution of the pipeline, are stored to a log file instead.
