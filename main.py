import re
import nltk
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer

def splitParagraph(content:str)->dict:
    paragraph = {}
    for i, line in enumerate(content.split("## ")):
        paragraph[i] = line
    return paragraph
    
def tokenize(content:str)-> str:
    return nltk.sent_tokenize(content)

# Fungsi untuk membersihkan teks
def preproccess(content : str)-> str:
    # Ubah teks menjadi huruf kecil
    content = content.lower()
    # Hapus tanda baca
    content = re.sub(r'[^\w\s]', '', content)
    return content

def summarize(text, top_n=2):
    return 
    
if __name__ == "__main__":
    with open('article.md', 'r', encoding='utf-8') as file:
        content = file.read()
        query = [text for text in content.splitlines() if text.startswith('# ')]
        # print(content) # untuk melihat isi article keseluruhan
        # print(query) # untuk melihat isi query
        paragraph = splitParagraph(content)
        
        for key, value in paragraph.items():
            print(f"Paragraph {key}: {value}\n")
