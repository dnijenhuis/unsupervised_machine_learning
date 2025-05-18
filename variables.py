# This module contains the variables/configs used by other modules.

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Variables for retrieving the data. The first file is the .GZ-file with the lowest number. The last file is the
# file with the highest number.
first_file = 1100
last_file = 1274

# URL and folders.
base_url = "https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
destination_folder = "PLACEHOLDER"
csv_folder = "PLACEHOLDER"

# Multi hot encoding variables. The top N most used Keywords, MeSH-terms and Chemicals that are added to the combined
# feature table. This data is used by the module 'transform_categorical_to_binary'.
top_n_keywords=100
top_n_mesh= 100
top_n_chemicals= 50

# TF-IDF config for clustering (!) input.
title_max_features = 50
title_ngram_range = (1, 2)

abstract_max_features = 50
abstract_ngram_range = (1, 2)

min_df_clustering = 500 # Only include terms that appear in at least N documents (so titles, abstracts).
max_df_clustering = 0.7 # Exclude terms that appear in more than X% of all documents.

# TF-IDF config for profiling (!).
tfidf_chunk_size = 125000  # number of rows processed.
title_abstract_max_features = 100
title_abstract_ngram_range = (2, 2)

min_df_profiling = 500 # Only include terms that appear in at least N documents (so titles, abstracts).
max_df_profiling = 0.5 # Exclude terms that appear in more than X% of all documents.

# Profiling configs. The number of top 'N' terms displayed per cluster/profile.
profiling_number_of_top_keywords = 3
profiling_number_of_top_mesh = 3
profiling_number_of_top_chemicals = 3
profiling_number_of_top_words_in_title_abstract = 3

# The following stop words are used by the TF-IDF on Title and Abstract (separately) and ('Title' + 'Abstract').
# This should prevent clustering articles based on domain specific 'stop words'.  The selection of these words has
# been done manually based on iterations. Only 'single' terms are included, no combinations. This is the format that
# TF-IDF requires from a set of stopwordss.
CUSTOM_DOMAIN_STOPWORDS_TF_IDF = ENGLISH_STOP_WORDS.union(set([
    "study", "effect", "effects", "analysis", "trial", "patients", "group", "data", "results",
    "evaluation", "based", "impact", "associated", "association", "human", "case", "cases",
    "review", "systematic", "prognosis", "meta", "meta-analysis", "risk", "factors", "objective",
    "report", "therapy", "models", "model", "retrospective", "prospective", "outcome", "outcomes",
    "cross", "sectional", "surveys", "survey", "questionnaires", "induced", "using", "high",
    "disease", "clinical", "patient", "care", "new", "relation", "related", "development",
    "animals", "animal", "male", "female", "mice", "rats", "inbred", "c57bl", "swine", "humans",
    "controlled", "randomized", "cohort", "prevalence", "population", "assessment", "assess",
    "type", "learning", "response", "literature", "enhanced", "insights", "biomarker", "biomarkers",
    "zebrafish", "women", "health", "treatment", "cell", "cells", "older", "acute", "correction",
    "qualitative", "disorder", "therapeutic", "year", "survival", "diagnosis", "classification",
    "mortality", "role", "properties", "performance", "potential", "management", "detection",
    "non", "single", "mendelian", "randomization", "trials", "topic", "cross-sectional", "studies",
    "syndrome", "novel", "research", "use", "medical", "19", "follow-up", "follow", "up", "early",
    "mediated", "activity",
    "12", "months", "95", "ci", "confidence", "interval", "adverse", "events", "decision", "making",
    "findings", "suggest", "logistic", "regression", "long", "term", "magnetic", "resonance", "odds",
    "ratio", "significant", "difference", "differences", "compared", "higher", "rate", "process",
    "effective", "conditions", "level", "levels", "methods", "including", "current", "significantly",
    "showed", "various", "respectively", "increased", "lower", "specific", "identified", "revealed",
    "reduced", "mechanisms", "species", "included", "001", "participants", "10", "total", "vs",
    "score", "mean",  "demonstrated", "changes", "control",
    "observed", "important", "provide", "multiple", "increase", "performed", "samples", "incidence",
    "time", "primary", "30", "05", "individuals", "overall", "groups", "evidence", "test", "statistically",
    "aimed", "investigate", "inclusion", "criteria", "real", "world", "self", "reported", "short",
    "pathway", "signaling", "web", "science", "mg", "kg", "old", "commonly", "used",
    "efficacy", "safety", "interquartile", "range", "large", "scale", "little", "known", "moderate",
    "severe", "ng", "ml", "operating", "characteristic", "pre", "post", "receiver", "semi",
    "structured", "sensitivity", "specificity", "state", "art", "remains", "unclear", "area", "curve",
    "did", "differ", "et", "al", "kaplan", "meier", "qualitative"
]))

# The following stop words are used by the profiling module. This prevents profiling clusters based on domain
# specific stop words. The selection of these words has been done manually based on iterations. Since the set is
# used for profiling, both single terms and combinations of terms are used (i.e. 'correlated' and
# 'positively correlated').
CUSTOM_DOMAIN_STOPWORDS_PROFILING = ENGLISH_STOP_WORDS.union(set([
    "study", "effect", "effects", "analysis", "trial", "patients", "group", "data",
    "disease", "treatment", "approach", "results", "evaluation", "based", "impact",
    "associated", "association", "human", "case", "review", "systematic", "studies",
    "prognosis", "meta", "meta-analysis", "risk", "factors", "objective", "report",
    "case report", "therapy", "animals", "animal", "male", "female", "mice", "rats",
    "mice, inbred c57bl", "rats, sprague-dawley", "swine", "humans", "retrospective",
    "prospective", "outcome", "outcomes", "china", "united states", "nude", "cross",
    "sectional", "surveys", "survey", "questionnaires", "induced", "model", "using",
    "high", "clinical", "patient", "care", "new", "relation", "related", "development",
    "risk factors", "survival", "diagnosis", "classification",
    "systematic review", "role", "properties", "performance", "potential", "management",
    "detection", "assessment", "non", "single", "mendelian randomization", "prospective studies",
    "randomized controlled trials as topic", "cross-sectional studies", "syndrome", "novel",
    "research", "use", "medical", "19", "follow-up studies", "prevalence", "controlled",
    "cohort", "early", "mediated", "activity", "randomized", "population", "type", "learning",
    "response", "literature", "enhanced", "insights", "biomarker", "biomarkers", "zebrafish",
    "women", "health", "retrospective studies", "treatment outcome", "cell", "cells", "older",
    "acute", "correction", "qualitative", "disorder", "therapeutic", "surveys and questionnaires",
    "year", "disease models, animal", "adsorption", "low",
    "method", "time", "different", "used", "positively correlated",
    "limit of detection", "significant", "median follow",
    "compared", "higher", "10", "rate", "process", "effective", "conditions", "level",
    "methods", "including", "current", "significantly", "showed", "various", "respectively",
    "increased", "lower", "specific", "identified", "revealed", "reduced", "findings",
    "mechanisms", "species", "ci", "95", "95 ci", "included", "years", "001", "participants",
    "12", "total", "vs", "score", "mean",  "infant, newborn",
    "demonstrated", "changes", "control", "observed", "important", "provide", "multiple",
    "increase", "performed", "samples", "cohort studies", "incidence", "time factors",
    "risk assessment", "primary", "months", "conducted", "30", "05", "individuals", "overall",
    "groups", "levels", "rates", "aimed", "evidence", "test", "vitro vivo"
    "previous studies", "future studies", "recent years", "reproducibility of results",
    "growth factor", "growth", "mass index", #body mass index was recognized twice, as "body mass"
    # and "mass index", since they are both bigrams. Though context giving, it is a duplicate.
    # Therefore, one of the two is taken out ("mass index").
    "mice, knockout", "influencing factors", "middle aged", "young adolescent", "young adult", "median age",
    "adolescent", "middle aged", "adult", "18 years", "aged 18", "predictive value of tests", "proposed method",
    "years age", "age sex", "65 years", "longitudinal studies", "different types", "length stay",
    "randomized controlled trial", "adolescents", "intervention", "cox proportional", "qualitative research",

]))

# Term normalization dictionary. This has been done manually based on iterations.
TERM_REPLACEMENTS = {
    "child, preschool": "child",
    "infant": "child",
    "children": "child",
    "child, newborn": "child",
    "child, preschool": "child",
    "older adults": "aged",
    "aged, 80 and over": "aged",
    "machine learning": "artificial intelligence",
    "deep learning": "artificial intelligence",
    "neural network": "artificial intelligence",
    "artificial intelligences, computer": "artificial intelligence",
    "artificial intelligences": "artificial intelligence",
    "sars-cov-2": "covid-19",
    "covid-19 pandemic": "covid-19",
    "sars-cov": "covid-19",
    "sars cov": "covid-19",
    "covid pandemic": "covid-19",
    "alzheimer disease": "alzheimer",
    "alzheimer’s disease": "alzheimer",# 2 different signs: ' versus ’. Annoying.
    "alzheimer's disease": "alzheimer" # 2 different signs: ' versus ’. Annoying.
}
