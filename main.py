import re
import nltk
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('punkt_tab')

def splitParagraph(content:str)->dict:
    paragraph = {}
    for i, line in enumerate(content.split("## ")):
        paragraph[i] = line
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
    # pecah menjadi beberapa dokumen
    docs = splitDocument(content)
    
    # tokenisasi teks
    for i, doc in enumerate(docs):
        tokens = tokenize(doc)
        print(f"Dokumen {i}: {tokens}")
        
    

def summarize(text, top_n=2):
    # split paragraph
    paragraphs = splitParagraph(text)
    final_summary = []
    for key, value in paragraphs.items():
        value = preproccess(value)
        sentences = tokenize(value)
        if len(sentences)<= 2:
                final_summary.extend(sentences)
                continue
    return final_summary
    
if __name__ == "__main__":
    with open('article.md', 'r', encoding='utf-8') as file:
        content = file.read()
        query = [text for text in content.splitlines() if text.startswith('# ')]
        # print(content) # untuk melihat isi article keseluruhan
        # print(query) # untuk melihat isi query
        paragraph = splitParagraph(content)
        
        # for key, value in paragraph.items():
        #     print(f"Paragraph {key}: {value}\n")
        for key, value in paragraph.items():
            print(f"Paragraph {key}\n")
            preproccess(value)
