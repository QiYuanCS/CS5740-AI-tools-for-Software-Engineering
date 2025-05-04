import glob

import glob

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# Load all data files matching 'data/datasets/train-00000-5k-2*.parquet'.
# Merge those dataframes into a single dataframe "df".


# Get the list of file paths matching the pattern

# Initialize an empty list to store the dataframes

# Iterate over each file path, read them in (parquet files) and append them to the list

# Concatenate all the dataframes into a single dataframe

# Define a variable code_snippets (from data frames's "code" attribute)

# Define labels (from dataframe's "language" attribute)

# Convert code snippets to TF-IDF features using TfidfVectorizer
# Display the shape of the TF-IDF features

# Perform K-Means clustering

# Group the code snippets into clusters.  A cluster is a dictionary with the cluster number as the key and a list of code snippets as the value.

# Iterate through each cluster and print the cluster's label and the first 5 code snippets in the cluster.
# Use up to 100 characters to print for each snippet.
# If any example snippet has embedded newline characters, eliminate them and replace with a space.


# Print the number of clusters
# Print the number of code snippets in each cluster
# Print the number of code snippets in each language in each cluster
# Print the number of code snippets in each language across all clusters

# Load all data files matching the pattern
file_paths = glob.glob('data/datasets/train-00000-5k-2*.parquet')

# Initialize an empty list to store the dataframes
dataframes = []

# Iterate over each file path, read the parquet files, and append them to the list
for file_path in file_paths:
    df = pd.read_parquet(file_path)
    dataframes.append(df)

# Concatenate all the dataframes into a single dataframe
df = pd.concat(dataframes, ignore_index=True)

# Define the variables
code_snippets = df['code']
labels = df['language']

# Convert code snippets to TF-IDF features
vectorizer = TfidfVectorizer()
tfidf_features = vectorizer.fit_transform(code_snippets)
print(f"Shape of TF-IDF features: {tfidf_features.shape}")

# Perform K-Means clustering
num_clusters = 5  # Define the number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(tfidf_features)

# Group the code snippets into clusters
clusters = {}
for i, label in enumerate(kmeans.labels_):
    clusters.setdefault(label, []).append(code_snippets.iloc[i])

# Iterate through each cluster and print the cluster's label and first 5 code snippets
for cluster_label, snippets in clusters.items():
    print(f"\nCluster {cluster_label}:")
    for snippet in snippets[:5]:
        print(f"  - {snippet.replace('\n', ' ')[:100]}")

# Print the number of clusters
print(f"\nNumber of clusters: {num_clusters}")

# Print the number of code snippets in each cluster
for cluster_label, snippets in clusters.items():
    print(f"Cluster {cluster_label} has {len(snippets)} code snippets.")

# Print the number of code snippets in each language in each cluster
print("\nNumber of code snippets in each language for each cluster:")
for cluster_label, snippets in clusters.items():
    language_counts = df.iloc[[df['code'].tolist().index(snippet) for snippet in snippets]]['language'].value_counts()
    print(f"Cluster {cluster_label}:")
    print(language_counts)

# Print the number of code snippets in each language across all clusters
print("\nNumber of code snippets in each language across all clusters:")
print(df['language'].value_counts())


my_cluster_theory = """
The clusters are likely defined based on the content and structure of the code snippets. 
The TF-IDF vectorizer captures the frequency and importance of terms within each snippet, 
allowing the K-Means algorithm to group similar snippets together based on their textual features.

For example, clusters may represent:
1. Specific programming languages: Snippets written in Python, Java, or C++ may have distinct patterns, 
   syntax, and keywords that are identified by the vectorizer and grouped into separate clusters.
2. Functional similarity: Code performing similar operations, such as file I/O, data processing, or API calls, 
   might use similar terminology and structure, causing them to fall into the same cluster.
3. Complexity or style: More complex or structured code may form separate clusters from simpler scripts, 
   as their token distribution and term importance could differ significantly.

Overall, each cluster is defined by patterns in token usage, frequency, and distribution across the snippets, 
which may correlate with programming language, functionality, or coding style.
"""
print(f"\nCluster Theory:\n\n{my_cluster_theory}\n\n")
