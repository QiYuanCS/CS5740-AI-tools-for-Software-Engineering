# TF-IDF Example
# In this example, we will use the TfidfVectorizer class from scikit-learn
# to convert a corpus of text documents into TF-IDF vectors.
# We will then print the TF-IDF vectors and the feature names.
#
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# print with more than 70 characters wide
np.set_printoptions(linewidth=200)

def main():
	# Define the corpus
	corpus = [
		"I love programming in Python",
		"Python is a great programming language",
		"I love playing football",
	]

	# Initialize a TfidfVectorizer object
	vectorizer = TfidfVectorizer()

	# Generate the TF-IDF vectors for the corpus
	X = vectorizer.fit_transform(corpus)

	# Get feature names and print them aligned on 11 char boundaries with leading 2 spaces.
	feature_names = vectorizer.get_feature_names_out()
	print("  ", end="")
	for word in feature_names:
		truncated_word = word[:11]  # Truncate the word to 8 characters
		print(f"{truncated_word:<11}", end="")

	print()



	# Convert the matrix to an array and print the result
	print(X.toarray())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


#	corpus = [
#		"I love programming in Python",
#		"Python is a great programming language",
#		"I love playing football",
#	]

# ['football'  'great'    'in'       'is'       'language' 'love'         'playing'  'prog/ing' 'python']
# [[0.         0.         0.60465213 0.         0.         0.45985353     0.         0.45985353 0.45985353]
#  [0.         0.49047908 0.         0.49047908 0.49047908 0.             0.         0.37302199 0.37302199]
#  [0.62276601 0.         0.         0.         0.         0.4736296      0.62276601 0.         0.        ]]
