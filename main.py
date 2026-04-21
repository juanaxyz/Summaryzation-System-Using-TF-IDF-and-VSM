import re
import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

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
    document_text = " ".join(paragraphs.values())
    sentences = splitDocument(document_text)

    if not sentences:
        return []

    if len(sentences) <= top_n:
        return [s.strip() for s in sentences]

    cleaned_docs = preproccess(document_text)
    processed_sentences = [" ".join(tokens) for tokens in cleaned_docs]

    # Jika setelah preprocessing kalimat kosong, fallback ke kalimat awal.
    if not any(processed_sentences):
        return [s.strip() for s in sentences[:top_n]]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_sentences)
    sentence_scores = np.asarray(tfidf_matrix.sum(axis=1)).flatten()

    ranked_idx = np.argsort(sentence_scores)[::-1][:top_n]
    selected_idx = sorted(ranked_idx)
    final_summary = [sentences[i].strip() for i in selected_idx]
    return final_summary
    
if __name__ == "__main__":
    with open('article.md', 'r', encoding='utf-8') as file:
        content = file.read()
        query = [text for text in content.splitlines() if text.startswith('# ')]
        query = preproccess(query[0]) # untuk mengambil judul artikel dan membersihkan teksnya
        # print(content) # untuk melihat isi article keseluruhan
        print(query) # untuk melihat isi query
        paragraph = splitParagraph(content)
        # print(paragraph)
    
        # for key, value in paragraph.items():
        #     print(f"Paragraph {key}: {value}\n")
        for key, value in paragraph.items():
            print(f"Paragraph {key + 1}\n")
            # print(f"original paragraph = {value}\n")
            clear_docs = preproccess(value)
            # print(f"clear paragraph = {clear_docs}\n")
            
            # untuk melihat hasil preproccessing dari setiap paragraf dalam tabel
            formated_data = []
            for i, words in enumerate(clear_docs):
                formated_data.append({'dokumen': i + 1, 'Words': words})
            df = pd.DataFrame(formated_data, columns=['dokumen', 'Words'])
            print(df)
            
            
