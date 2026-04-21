import re
import nltk
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


def splitParagraph(content:str)->dict:
    paragraph = {}
    # hapus judul artikel yang menggunakan # pada awalnya
    content = re.sub(r'^#\s+.*\n?', '', content, count=1, flags=re.MULTILINE)

    for i, line in enumerate(content.split("## ")):
        clean_line = line.strip()
        if clean_line:
            paragraph[len(paragraph)] = clean_line
    return paragraph


def getTitle(content: str) -> str:
    for line in content.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return ""
    
def splitDocument(content :str) :
    sentences = nltk.sent_tokenize(content)
    return sentences


def tokenize(content:str)-> str:
    tokens = nltk.word_tokenize(content)
    tokens = re.sub(r'[^\w\s]', '', ' '.join(tokens)).lower().split()
    return tokens

# Fungsi untuk membersihkan teks
def preproccess(content : str)-> str:
    list_stopwords = set(stopwords.words('english'))
    
    # pecah menjadi beberapa dokumen
    docs = splitDocument(content)
    clear_docs = []
    # print(docs)
    # tokenisasi teks
    for i, doc in enumerate(docs):
        tokens = tokenize(doc)
        # print(f"Tokens", tokens)
        clear_text = [w for w in tokens if w not in list_stopwords and w.isalnum()]
        # print(clear_text)
        clear_docs.append(clear_text)
    
    return clear_docs

    

def summarize(text, top_n=2):
    paragraphs = splitParagraph(text)
    title = getTitle(text)
    query_tokens = preproccess(title)
    query_doc = " ".join(query_tokens[0]) if query_tokens else ""

    final_summary = []

    for _, paragraph in paragraphs.items():
        sentences = splitDocument(paragraph)
        if not sentences:
            continue

        # Jika kalimat sedikit, langsung ambil semuanya.
        if len(sentences) <= top_n:
            final_summary.extend([s.strip() for s in sentences])
            continue

        cleaned_docs = preproccess(paragraph)
        processed_sentences = [" ".join(tokens) for tokens in cleaned_docs]

        # Jika query kosong atau kalimat kosong setelah preprocessing, fallback.
        if not query_doc or not any(processed_sentences):
            final_summary.extend([s.strip() for s in sentences[:top_n]])
            continue

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(processed_sentences + [query_doc])

        sentence_vectors = tfidf_matrix[:-1]
        query_vector = tfidf_matrix[-1]
        similarities = cosine_similarity(sentence_vectors, query_vector).flatten()

        top_k = min(top_n, len(sentences))
        ranked_idx = np.argsort(-similarities, kind='mergesort')[:top_k]

        for idx in ranked_idx:
            final_summary.append(sentences[idx].strip())

    return final_summary
    
if __name__ == "__main__":
    with open('article.md', 'r', encoding='utf-8') as file:
        content = file.read()
        summary = summarize(content, top_n=2)

        print("Summary:")
        for sentence in summary:
            print(f"- {sentence}")
            
            
