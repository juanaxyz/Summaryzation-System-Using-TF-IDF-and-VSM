import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
nltk.download('punkt')
ps = PorterStemmer()

text = """# What is Anthropic's Claude Mythos and what risks does it pose? 

16 hours ago

Liv McMahon,Technology reporterand

Joe Tidy,Cyber correspondent, BBC World Service

![](https://static.files.bbci.co.uk/bbcdotcom/web/20260407-092955-f3cfe0ee04-web-3.0.0-2/grey-placeholder.png)!Reuters A smartphone display showing the Anthropic logo in black letters on an all-white background, laid on a laptop keyboard lit in pink and purpleReuters

In recent weeks, the AI world has been a-buzz following claims made by leading firm, Anthropic, regarding its new model, Claude Mythos.

The company says it found the tool can outperform humans at some hacking and cyber-security tasks, which has prompted discussions by regulators, legislators and financial institutions about the dangers it could pose to digital services.

Several tech giants have been given access to Mythos via an initiative called Project Glasswing, designed to strengthen resilience to Mythos itself.

But others point out that it is in Anthropic's interests to suggest its tool has never-seen-before capabilities, meaning - as ever with AI - the job of distinguishing between justified claims and hype can be tricky.

## What is Claude Mythos?

Mythos is one of Anthropic's latest models developed as part of its broader AI system called Claude. It encompasses the company's AI assistant and family of models, rivalling OpenAI's ChatGPT and Google's Gemini.

It was revealed by Anthropic in early April as "Mythos Preview"."""


def splitParagraph(content: str) -> dict:
    # parts = re.split(r'\n(?=##? )', text)

    # # Membersihkan spasi kosong di awal/akhir tiap bagian
    # parts = [p.strip() for p in parts if p.strip()]

    paragraph = {}
    for i, line in enumerate(re.split(r'\n(?=##? )', content)):
        clean_line = line.strip()
        paragraph[i + 1] = clean_line
    return paragraph

def splitDocument(paragraph: str) -> list[str]:
    # 1. Split berdasarkan baris
    lines = paragraph.splitlines()
    
    clean_docs = []
    
    for line in lines:
        line = line.strip()
        
        # SKIP jika baris kosong
        if not line:
            continue
            
        # 1. HAPUS baris jika itu adalah Heading (# judul)
        if re.match(r'^\s*#{1,6}\s+', line):
            continue
            
        # 2. HAPUS baris jika dimulai dengan format gambar ![](...)
        # Kita gunakan re.match agar jika baris diawali gambar, seluruh baris dibuang
        if re.match(r'^!\[.*?\]\(.*?\)', line):
            continue
            
        # 3. FILTER tambahan untuk baris sampah (Optional)
        # Menghapus baris yang hanya berisi keterangan waktu atau reporter pendek
        # Contoh: "16 hours ago" atau baris yang terlalu pendek (kurang dari 20 karakter)
        if "hours ago" in line or "correspondent" in line or "reporter" in line:
            continue

        # 4. Jika lolos filter, masukkan ke list
        clean_docs.append(line)
        
    return clean_docs

def tokenize(text:str)-> list[str]:
    return word_tokenize(text)

def removeStopwords(tokens: list[str]) -> list[str]:
    # Membersihkan tanda baca di sekitar kata dan membuang kata jika ada di stopwords
    # string.punctuation berisi !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    
    clean_tokens = []
    for word in tokens:
        # Hapus tanda baca dari ujung-ujung kata (misal: "mytho." -> "mytho")
        word = word.strip(string.punctuation)
        
        # Masukkan ke list jika kata tidak kosong DAN bukan stopword
        if word and word.lower() not in stopwords :
            clean_tokens.append(word)
            
    return clean_tokens

def stemming(tokens: list[str]) -> list[str]:
    return [
        ps.stem(word)
        for word in tokens
        if word
    ]
    

def getTitle(content: str) -> str:
    for line in content.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return ""


def preProcess(sentence: str):
    sentence =sentence.lower()
    tokens = tokenize(sentence)
    # print(f"Tokens: {tokens}")
    tokens = removeStopwords(tokens)
    # print(f"Tokens after stopword removal: {tokens}")
    tokens = stemming(tokens)
    # print(f"Tokens after stemming: {tokens}")
    return tokens

if __name__ == "__main__":

    paragraph = splitParagraph(text)
    print(f"jumlah paragraf: {len(paragraph)}")
    print("===============================")
    for i, p in paragraph.items():
        print(f"--- BAGIAN {i} ---")
        print(p)
    
        print(f"-- SPLIT DOCUMENT ---")
        sentences = splitDocument(p)
        print(sentences)
        print(f"-- PREPROCESS ---")
        for s in sentences:
            print(f"Kalimat: {s}")
            print(f"Preprocessed: {preProcess(s)}")
            print("===============================")
