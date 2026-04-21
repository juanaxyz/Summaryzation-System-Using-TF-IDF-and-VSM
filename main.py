import re
import nltk
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


def splitParagraph(content: str) -> dict:
    content = re.sub(r'^#\s+.*$', '', content, flags=re.MULTILINE).strip()
    paragraph = {}
    for line in content.split("## "):
        clean_line = line.strip()
        if clean_line:
            paragraph[len(paragraph)] = clean_line
    return paragraph

def getTitle(content: str) -> str:
    for line in content.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return ""


def splitDocument(content: str) -> list[str]:
    content = re.sub(r'^\s*#{1,6}\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'(\*{1,2}|_{1,2})(.*?)\1', r'\2', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    lines = content.splitlines()
    if lines and not re.search(r'[.!?]$', lines[0].strip()):
        content = '\n'.join(lines[1:]).strip()

    if not content:
        return []

    sentences = nltk.sent_tokenize(content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return sentences

def tokenize(content:str)-> str:
    tokens = nltk.word_tokenize(content)
    tokens = re.sub(r'[^\w\s]', '', ' '.join(tokens)).lower().split()
    return tokens


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
    query_doc = " ".join([tok for sent in query_tokens for tok in sent])

    final_summary = []

    for _, paragraph in paragraphs.items():
        # print(f"paragraph : {paragraph}")
        # print("====="*20)
        sentences = splitDocument(paragraph)
        
        # print(f"Sentences: {sentences}")
        # print("====="*20)
        
        if not sentences:
            continue

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

        ranked_idx_sorted = sorted(ranked_idx)
        for idx in ranked_idx_sorted:
            final_summary.append(sentences[idx].strip())

    return final_summary
    
if __name__ == "__main__":
    with open('article.md', 'r', encoding='utf-8') as file:
        content = file.read()
        summary = summarize(content, top_n=2)

        print("Summary:")
        for sentence in summary:
            print(f"- {sentence}")
            
            
