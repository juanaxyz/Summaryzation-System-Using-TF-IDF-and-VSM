import re

def splitParagraph(content:str)->dict:
    paragraph = {}
    for i, line in enumerate(content.split("## ")):
        paragraph[i] = line
    return paragraph
    
def tokenize(content:str)-> str:
    return 

def preproccess(content : str)-> str:
    return 

if __name__ == "__main__":
    with open('article.md', 'r') as file:
        content = file.read()
        query = [text for text in content.splitlines() if text.startswith('# ')]
        # print(content) # untuk melihat isi article keseluruhan
        # print(query) # untuk melihat isi query
        paragraph = splitParagraph(content)
        
        for key, value in paragraph.items():
            print(f"Paragraph {key}: {value}\n")
