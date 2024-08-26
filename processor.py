from tkinter.constants import TRUE
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from excel_update import fetch_data_to_csv

# Downloading necessary nltk data
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

df = None
vectorizer = None
tfidf_matrix = None

def preprocess(text: str):
  tokens = word_tokenize(text.lower())
  filtered_tokens = []
  for token in tokens:
    if token not in string.punctuation and token not in stopwords.words("english"):
      filtered_tokens.append(token)

  return " ".join(filtered_tokens)

def update_tfidf():
  global df, vectorizer, tfidf_matrix
  df = fetch_data_to_csv()
  if df is not None:
    rel_column = "One-liner"

    df["processed_text"] = df[rel_column].apply(preprocess)
    vectorizer = TfidfVectorizer()

    # TF-IDF matrix shape: (|D|, |V|)
    # element (i, j) represents TF-IDF score for i-th word from the vocabulary w.r.t the j-th document/record.
    tfidf_matrix = vectorizer.fit_transform(df["processed_text"])

def periodic_update():
    while True:
        try:
            update_tfidf()
        except Exception as e:
            print(f"An Error occurred during the update: {e}")
        time.sleep(1800)

def search(query, top_k=3):
    global df, vectorizer, tfidf_matrix
    
    if df is None or vectorizer is None or tfidf_matrix is None:
        return "Data is still loading. Please try again in a moment."
      
    processed_query = preprocess(query)
  
    # shape (1, |V|), where |V| is the size of the vocabulary across the corpus
    query_vec = vectorizer.transform([processed_query])

    # getting the similarity between the query vector and each document's TF-IDF vector
    # shape is (1, |D|) – denotes the cosine similarty between the singular query vector 
    # and every document's TF-IDF vector (i.e. a row from the TF-IDF matrix)
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix)

    # gets the indices that would sort the array, and returns the last k of them
    # since they correspond to the rows with the largest cosine similarities

    # the flipping is to get the most relevant results
    top_indices = cosine_similarities.flatten().argsort()[-top_k:][::-1]

    # returns the rows of teh dataframe as Series objects
    return df.iloc[top_indices]


def gradio_search(query):
    results = search(query)
  
    if isinstance(results, str):  # Error message
        return results
  
    output = ""
    for i, (_, row) in enumerate(results.iterrows(), 1):
        output += f"\nResult {i}:\n"
        for column in df.columns:
            output += f"\t{column}: {row[column]}\n"
        output += "-" * 50 + "\n"
    return output

# initial data load
update_tfidf()
