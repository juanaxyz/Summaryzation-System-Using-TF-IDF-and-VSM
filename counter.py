import math
from collections import Counter

# doc = ['in', 'recent', 'week', ',', 'ai', 'world', 'a-buzz', 'follow', 'claim', 'made', 'lead', 'firm', ',', 'anthrop', ',', 'regard', 'new', 'model', ',', 'claud', 'mytho', '.', 'ai']
# query_tokens = ['ai', 'model', 'anthrop', 'claud']

def tf_counter(term: list, document):
        """
        menghitung term frequency (TF) untuk sebuah term dalam sebuah dokumen.
        
        :param term: Term yang ingin dihitung frekuensinya (string).
        :param document: Dokumen yang akan dihitung (list of strings).
        :return: Nilai TF untuk term dalam dokumen (float).
        """
        return document.count(term)
            

def calc_df(term, corpus):
    """
    menghitung document frequency (DF) untuk sebuah term dalam sebuah korpus.
    
    :param term: Term yang ingin dihitung DF-nya (string).
    :param corpus: Korpus yang akan dihitung (list of list of strings).
    :return: Nilai DF untuk term dalam korpus (int).
    """
    return sum(1 for document in corpus if term in document)
    
def calc_idf(N, df):
    """
    menghitung inverse document frequency (IDF) untuk sebuah term dalam sebuah korpus.
    
    :param N: Jumlah dokumen dalam korpus (int).
    :param df: Document frequency untuk term tersebut (int).
    :return: Nilai IDF untuk term dalam korpus (float).
    """
    # return (math.log(N / df) + 1)  # Menambahkan 1 untuk menghindari pembagian dengan nol
    return math.log(N  / df) + 1  # Menambahkan 1 untuk menghindari pembagian dengan nol
    
def calc_cosine_similarity(dot_product, magnitude_vec1, magnitude_vec2):
    """
    menghitung cosine similarity antara dua vektor.
    
    :param dot_product: Hasil perkalian titik antara dua vektor (float).
    :param magnitude_vec1: Magnitudo dari vektor pertama (float).
    :param magnitude_vec2: Magnitudo dari vektor kedua (float).
    :return: Nilai cosine similarity antara dua vektor (float).
    """
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0.0  # Menghindari pembagian dengan nol
    return dot_product / (magnitude_vec1 * magnitude_vec2)
    

class tfIDfCalculations:
    def __init__(self):
        pass
    
    def calc_tf(self, term, document):
        """
        menghitung term frequency (TF) untuk sebuah term dalam sebuah dokumen.
        
        :param term: Term yang ingin dihitung frekuensinya (string).
        :param document: Dokumen yang akan dihitung (list of strings).
        :return: Nilai TF untuk term dalam dokumen (float).
        """
        return document.count(term)
    