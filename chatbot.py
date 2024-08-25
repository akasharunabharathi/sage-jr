import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Downloading necessary nltk data
nltk.download("punkt")
nltk.download("stopwords")

# Load the CSV file
df = pd.read_csv("/content/sage-jr/latest_excel_data.csv")

# Relevant column
rel_column = "One-liner"

def preprocess(text: str):
  tokens = word_tokenize(text.lower())
  filtered_tokens = []
  for token in tokens:
    if token not in string.punctuation and token not in stopwords.words("english"):
      filtered_tokens.append(token)

  return " ".join(filtered_tokens)

df["processed_text"] = df[rel_column].apply(preprocess)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["processed_text"])

def search(query, top_k=3):
    processed_query = preprocess(query)
    query_vec = vectorizer.transform([processed_query])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = cosine_similarities.argsort()[-top_k:][::-1]
    return df.iloc[top_indices], cosine_similarities[top_indices]

def gradio_search(query):
    results, similarities = search(query)
    output = ""
    for i, (_, row) in enumerate(results.iterrows(), 1):
        output += f"\nResult {i} (Similarity: {similarities[i-1]:.4f}):\n"
        for column in df.columns:
            if column not in ['processed_text']:
                output += f"{column}: {row[column]}\n"
        output += "-" * 50 + "\n"
    return output
