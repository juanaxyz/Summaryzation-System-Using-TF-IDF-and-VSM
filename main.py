import re
import nltk
import math
from nltk.corpus import stopwords
import numpy as np
from collections import Counter


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')


def splitParagraph(content: str) -> dict:
    # Hapus Heading Utama (# Judul) lalu pecah berdasarkan subheading (## Subjudul)
    content = re.sub(r'^#\s+.*$', '', content, flags=re.MULTILINE).strip()
    paragraph = {}
    for line in content.split("## "):
        clean_line = line.strip()
        if clean_line:
            paragraph[len(paragraph)] = clean_line
    return paragraph

def getTitle(content: str) -> str:
    #ambil baris pertama yang diawali dengan '# ' sebagai judul utama
    for line in content.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return ""


def splitDocument(content: str) -> list[str]:
    content = re.sub(r'^\s*#{1,6}\s+.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'(\*{1,2}|_{1,2})(.*?)\1', r'\2', content)
    content = re.sub(r'!?\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'["\u201c\u201d]', '', content)
    content = re.sub(r',', '', content)
    content = content.strip()

    # Jika baris pertama bukan kalimat lengkap (tidak diakhiri . ! ?), lewati
    lines = content.splitlines()
    if lines and not re.search(r'[.!?]$', lines[0].strip()):
        content = '\n'.join(lines[1:]).strip()

    if not content:
        return []

    # Pecah menjadi kalimat menggunakan nltk
    sentences = nltk.sent_tokenize(content)
    # Hapus kalimat yang terlalu pendek (misalnya kurang dari 20 karakter)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return sentences

def tokenize(content:str)-> str:
    # word tokenization dengan nltk, lalu hapus tanda baca dan ubah ke lowercase
    tokens = nltk.word_tokenize(content)
    tokens = re.sub(r'[^\w\s]', '', ' '.join(tokens)).lower().split()
    return tokens


def preproccess(content : str)-> str:
    list_stopwords = set(stopwords.words('english'))
    
    # pecah menjadi beberapa dokumen atau kalimat dengan splitDocument
    docs = splitDocument(content)
    clear_docs = []

    for i, doc in enumerate(docs):
        tokens = tokenize(doc)
        # print(f"Tokens", tokens)
        clear_text = [w for w in tokens if w not in list_stopwords and w.isalnum()]
        # print(clear_text)
        clear_docs.append(clear_text)
    
    return clear_docs

def compute_tf(tokens: list) -> dict:
    
    """
    TF(t, d) = f(t, d) / jumlah_total_token(d)
    Mengukur seberapa sering sebuah term muncul dalam satu dokumen.
    """

    total = len(tokens)
    if total == 0:
        return {}
    
    # Hitung frekuensi kata (token)
    counts = Counter(tokens)
    return {word: count/ total for word, count in counts.items()}

def compute_idf(documents: list) -> dict:
    """
    IDF(t) = log( (N+1) / (df(t)+1) ) + 1
    Mengukur seberapa jarang sebuah term muncul di seluruh dokumen.
    Term yang jarang = lebih informatif = IDF lebih tinggi.
    Smoothing (+1) mencegah pembagian nol.
    """

    N = len(documents)
    
    df = {}
    for tokens in documents:
        for term in set(tokens):
            df[term] = df.get(term, 0) + 1
            
    idf = {}
    for term, count in df.items():
        idf[term] = math.log((N + 1) / (count + 1)) + 1
        
    return idf

def compute_tfidf_vector(tokens: list, idf: dict) -> dict:
    """
    TF-IDF(t, d) = TF(t, d) * IDF(t)
    Representasi vektor sebuah dokumen — semakin tinggi nilainya,
    semakin penting term tersebut dalam dokumen ini.
    """

    tf = compute_tf(tokens)
    
    # nilai IDF fallback untuk term yang tidak muncul di dokumen lain (df=0) adalah log( (N+1) / (0+1) ) + 1
    idf_fallback = math.log(1 + 1) / (0 + 1) + 1 
    
    vector = {}
    for term, tf_val in tf.items():
        idf_val = idf.get(term, idf_fallback)
        vector[term] = tf_val * idf_val
        
    return vector

def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """
    cos(A, B) = (A · B) / (||A|| x ||B||)
    Mengukur kemiripan arah dua vektor — nilainya 0.0 (tidak mirip) hingga 1.0 (identik).
    Digunakan untuk mengukur relevansi kalimat terhadap query (judul).
    """

    dot_product = sum(vec_a.get(term, 0) * val for term, val in vec_b.items())
    
    magnitude_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    magnitude_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)

    
def summarize(text, top_n=2):
    paragraphs = splitParagraph(text)
    title = getTitle(text)

    # query di ambil dari judul utama - representasi topic utama document, lalu di tokenisasi dan stopword dihapus
    stop_words = set(stopwords.words('english'))
    query_tokens = tokenize(title)
    query_tokens = [w for w in query_tokens if w not in stop_words and w.isalnum()]

    final_summary = []

    for _, paragraph in paragraphs.items():
        sentences = splitDocument(paragraph)

        if not sentences:
            continue
        
        # paragraph yang terlalu pendek (misalnya hanya 1 kalimat) langsung diambil semua tanpa skor, karena tidak perlu diranking
        if len(sentences) <= top_n:
            for s in sentences:
                final_summary.append({"kalimat": s.strip(), "skor": None})
            continue

        cleaned_docs = preproccess(paragraph)

        # Fallback: jika semua kalimat kosong setelah preprocessing
        if not any(cleaned_docs):
            for s in sentences[:top_n]:
                final_summary.append({"kalimat": s.strip(), "skor": None})
            continue

        all_docs_for_idf = cleaned_docs + [query_tokens]
        idf = compute_idf(all_docs_for_idf)

        if not query_tokens:
            for s in sentences[:top_n]:
                final_summary.append({"kalimat": s.strip(), "skor": None})
            continue
        
        # Bangun vektor TF-IDF untuk setiap kalimat dan query
        sentence_vectors = [compute_tfidf_vector(tokens, idf) for tokens in cleaned_docs]
        query_vector = compute_tfidf_vector(query_tokens, idf)
        
        # Hitung cosine similarity setiap kalimat terhadap query
        similarites = [cosine_similarity(query_vector, sent_vec) for sent_vec in sentence_vectors]

        # pilih top_n kalimat dengan skor tertinggi, lalu urutkan kembali berdasarkan posisi asli di paragraf
        top_k = min(top_n, len(sentences))
        ranked_idx = sorted(range(len(similarites)), key=lambda i: similarites[i], reverse=True)[:top_k]
        ranked_idx_sorted = sorted(ranked_idx)

        
        for idx in ranked_idx_sorted:
            final_summary.append({
                "kalimat": sentences[idx].strip(),
                "skor": round(similarites[idx], 4)
            })

    return final_summary
    
if __name__ == "__main__":
    with open('article.md', 'r', encoding='utf-8') as file:
        content = file.read()
        summary = summarize(content, top_n=2)

        print("Summary:")
        for sentence in summary:
            print(f"- {sentence}")
            
            
