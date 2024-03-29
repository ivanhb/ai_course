# -*- coding: utf-8 -*-
"""nlp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d090c3Ae8UTmyudEZdUbPhoieQU2nOAl

## 2) Text preprocessing

Init the basic data and methods
"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk import pos_tag, ne_chunk
from nltk.parse import CoreNLPParser
from nltk.chunk import tree2conlltags
from nltk.tag import StanfordNERTagger

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

raw_text = "Artificial intelligence has revolutionized various industries, from healthcare to finance, by enabling advanced data analysis and decision-making capabilities."

"""#### Tokenization
Text is converted into smaller pieces called tokens. This is done at word level (word tokenization) or sentence level (sentence tokenization) depending on the analysis task.
"""

tokens = word_tokenize(raw_text)
print("Tokens:", tokens)

"""#### Stop Word Removal
Common words like "the" and "is," known as stop words, are removed. These words don't add much meaning and can clutter the analysis.
"""

stop_words = set(stopwords.words('english'))

filtered_tokens = []
for word in tokens:
    word_lower = word.lower()
    if word_lower not in stop_words:
        filtered_tokens.append(word_lower)

print("Filtered tokens: ",filtered_tokens)

"""#### Stemming/Lemmatization
Words are simplified to their root form. stemming removes prefixes and suffixes, while lemmatization uses a dictionary to find the base form. This helps standardize the text for easier analysis.
"""

ps = PorterStemmer()

stemmed_tokens = []
for word in filtered_tokens:
    stemmed_tokens.append(ps.stem(word))

print("Stemmed tokens: ",stemmed_tokens)

"""#### Lowercasing [SKIP]
Text is converted to lowercase. Since uppercase/lowercase can sometimes affect analysis, this ensures uniformity.

#### Language Detection [SKIP]
For multilingual content, the language of the text is identified. This helps tailor the analysis to the specific language nuances.

#### POS tagging

categorizing words in the text into grammatical classes such as nouns, verbs, and adjectives. This operation offers insights into the syntactic structure.

*Noun Tags:*
* NN: Noun (singular or common)
* NNS: Noun (plural)
* NNP: Proper noun (singular)
* NNPS: Proper noun (plural)

*Verb Tags:*
* VB: Verb (base form)
* VBD: Verb (past tense)
* VBG: Verb (gerund or present participle)
* VBP: Verb (past participle)
* VBZ: Verb (third person singular present)

*Adjective Tags:*
* JJ: Adjective
* JJR: Adjective (comparative)
* JJS: Adjective (superlative)

*Adverb Tags:*
* RB: Adverb
* RBR: Adverb (comparative)
* RBS: Adverb (superlative)

...
"""

pos_tags = pos_tag(tokens)
print("POS tags: ")
for element in pos_tags:
        print(element)

"""#### Parsing [SKIP]
Examining the grammatical arrangement of the sentences to recognize connections between words and establish the syntactic roles and dependencies

#### Coreference Resolution
Addressing references within the text by connecting pronouns or noun phrases to their corresponding entities, ensuring a cohesive understanding and analysis

## 3) Feature Engineering

### 3.1) Bag of Words BoW
"""

from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "The quick brown fox jumps over the lazy dog.",
    "The dog is lazy. The fox is quick and brown."
]

# Create an instance of CountVectorizer
vectorizer = CountVectorizer()

# Fit and transform the documents into a bag-of-words matrix
X = vectorizer.fit_transform(documents)

# Generate the vocabulary
vocabs = vectorizer.get_feature_names_out()

# Convert the bag-of-words matrix to a dense array
# (for readability reasons)
dense_array = X.toarray()

# Display the results
print("Vocabulary:", vocabs)
print("Bag-of-Words Matrix:")
print(dense_array)

"""### 3.2) Word embeddings and Word2Vec"""

from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


# Sample sentences
#sentences = [
#    "Machine learning algorithms, including neural networks, play a pivotal role in natural language processing tasks.",
#    "The rapid advancement of technology has transformed the way we interact with information and communicate in the digital era.",
#    "Data privacy concerns have become increasingly prominent as more personal information is shared and stored online.",
#    "Artificial intelligence applications, such as virtual assistants and chatbots, are reshaping user experiences across various industries.",
#    "The integration of automation and artificial intelligence is revolutionizing the landscape of modern manufacturing processes."
#]

# Tokenize the sentences into words
#okenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]

tokenized_sentences = [
    ["king", "queen", "ruler", "country"],
    ["happy", "joy", "sad", "gloomy"],
    ["computer", "science", "technology", "research"]
]

# Create Word2Vec model
model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, min_count=1, workers=4)

# Extract word vectors
word_vectors = [model.wv[word] for word in model.wv.key_to_index]

# Apply PCA to reduce dimensionality to 2D
pca = PCA(n_components=2)
pca_result = pca.fit_transform(word_vectors)

# Create a scatter plot
plt.figure(figsize=(10, 8))
plt.scatter(pca_result[:, 0], pca_result[:, 1])

# Annotate points with words
for i, word in enumerate(model.wv.key_to_index):
    plt.annotate(word, xy=(pca_result[i, 0], pca_result[i, 1]))

plt.title('Word Embeddings Visualization')
plt.show()

"""## 4) Modeling using ML: SVM  """

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC

# 1) Data acquisition
# Simple Dataset
emails = [
    "This is a legitimate email.",
    "Get rich quick! Click this link!",
    "Hi, how are you doing?",
    "Buy these amazing products now!"]

labels = [
    "non-spam",
    "spam",
    "non-spam",
    "spam"]


# 2) Preprocessing
# Remove stop words


# 3) Feature engineering
vectorizer = CountVectorizer()
features = vectorizer.fit_transform(emails)


# 4) Modelling

# 4.1) Train the SVM model
clf = SVC()
clf.fit(features, labels)

# 4.2) New email to classify
#new_email = "Free money, buy these amazing products now, and get rich down down down"
new_email = "How are you mr president"

new_features = vectorizer.transform([new_email])

# Predict the class
prediction = clf.predict(new_features)[0]
print("This email is classified as: ",prediction)