# Write a script that loads successively larger data files and merges them into larger training sets.
# For each training set, let's track training time, prediction time, and accuracy.
import glob
import pickle
import time

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import matplotlib.pyplot as plt

# Track measurements for each round: the round number/index, how long in seconds the train, predict steps take, and an accuracy report
# Use a list of dictionaries for measurement storage, with "round", "train", "predict", "accuracy" as keys


# Write a function named learn that takes a dataframe and an index as parameters.
# The index indicates the round number of learning. The function should:
# 1. Create a dictionary to store the measurements for this round
# 2. Print a message indicating the round number
# 3. Store the round number in the dictionary under 'round'
# 4. Split the dataframe into code snippets and labels
# 5. Split the code snippets and labels into training and test sets
# 6. Create a TF-IDF vectorizer
# 7. Use the 'fit_transform' method on the training data to learn the vocabulary and idf, and return term-document matrix.
# 8. Use the 'transform' method on the test data to transform documents to document-term matrix.
# 9. Create a Support Vector Machine classifier
# 10. Train the classifier using the training data
# 11. Save the model to a file and load it back from a file (to make sure it works)
# 12. Use the classifier to predict the labels for the test data
# 13. Print the classification report which should be a dictionary
# 14. Store the training time in the dictionary under 'train'
# 15. Store the prediction time in the dictionary under 'predict'
# 16. Store the classification report in the dictionary under 'report'
# 17. Add 'accuracy' to the dictionary and set it to the accuracy score from the classification report
# 18. Append the dictionary to the measurements list for this round


# Load all data files matching 'data/datasets/train-00000-5k*.parquet'.
# For each file loaded, merge the latest data file with the merged data to date,
# and call the learn function with the dataframe and the index of the file in the list of files.


# If I have measurements in Python like a list of dictionaries such as:
# [{'round': 0, 'train': 32.76, 'predict': 2.13, 'accuracy': 0.78},....]
# let us plot lines on the same graph for tfidf, train, predict and accuracy using python?  Use matplotlib.
# Add a legend.  Add axis labels.  Add a title.
# Lets save the plot to a file "supervised.png" before showing the plot.

# Initialize a list to store measurements for each round
measurements = []


def learn(dataframe, index):
    """
    Learn from the given dataframe and track the round measurements.

    Parameters:
    - dataframe: The input dataframe containing 'code' and 'language'.
    - index: The current round number.
    """
    # Create a dictionary to store measurements for this round
    measurement = {}
    print(f"Starting round {index}")
    measurement['round'] = index

    # Split the dataframe into code snippets and labels
    X = dataframe['code']
    y = dataframe['language']

    # Split into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a TF-IDF vectorizer and transform data
    vectorizer = TfidfVectorizer()
    start_time = time.time()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    measurement['tfidf_time'] = time.time() - start_time

    # Create an SVM classifier
    clf = SVC()
    start_time = time.time()
    clf.fit(X_train_tfidf, y_train)
    measurement['train'] = time.time() - start_time

    # Save and reload the model to verify
    with open('model.pkl', 'wb') as file:
        pickle.dump(clf, file)
    with open('model.pkl', 'rb') as file:
        clf = pickle.load(file)

    # Predict the labels for the test data
    start_time = time.time()
    y_pred = clf.predict(X_test_tfidf)
    measurement['predict'] = time.time() - start_time

    # Print and store the classification report
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=1)
    print(classification_report(y_test, y_pred, zero_division=1))
    measurement['report'] = report
    measurement['accuracy'] = accuracy_score(y_test, y_pred)

    # Append the measurements to the global list
    measurements.append(measurement)


# Load and process data files
merged_data = None
data_files = sorted(glob.glob('data/datasets/train-00000-5k*.parquet'))

for idx, file in enumerate(data_files):
    print(f"Loading file: {file}")
    data = pd.read_parquet(file)

    # Merge current data with the accumulated data
    if merged_data is None:
        merged_data = data
    else:
        merged_data = pd.concat([merged_data, data], ignore_index=True)

    # Call the learn function
    learn(merged_data, idx)

# Plot measurements
rounds = [m['round'] for m in measurements]
train_times = [m['train'] for m in measurements]
predict_times = [m['predict'] for m in measurements]
accuracies = [m['accuracy'] for m in measurements]

fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.plot(rounds, train_times, label='Training Time (s)', marker='o', color='blue')
ax1.plot(rounds, predict_times, label='Prediction Time (s)', marker='o', color='green')
ax1.set_xlabel('Round')
ax1.set_ylabel('Time (s)')

ax2.plot(rounds, accuracies, label='Accuracy', marker='o', color='red')
ax2.set_ylabel('Accuracy (0-1)')
ax2.set_ylim(0, 1)

fig.legend(loc='upper left')

plt.title('Supervised Learning Performance Over Rounds')
plt.grid()

plt.savefig('supervised.png')
plt.show()
