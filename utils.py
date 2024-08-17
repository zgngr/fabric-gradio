import string
from difflib import Differ

def diff_texts(text1, text2):
    text1, text2 = remove_punctuation(text1), remove_punctuation(text2)
    
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]

def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))

def count_lines_and_words(text):
    lines = text.splitlines()
    num_lines = len(lines)
    num_words = sum(len(line.split()) for line in lines)
    return num_lines, num_words