from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("corpus.txt", "r") as corp:
    corpus = corp.read()

def find_sentences(corpus):
    sentences = re.split(r'[.!?]', corpus)
    sentences = [sentence.strip().lower() for sentence in sentences if len(sentence.strip()) > 1]  
    sentences = [re.sub(r'[,.!?"\']', ' ', sentence) for sentence in sentences]
    sentences = [re.sub(r'\s{2,}', ' ', sentence) for sentence in sentences]
    return sentences

sentences = find_sentences(corpus)

def p_of_a_given_b(a, sentences):
    next_word_counts = {}
    
    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words) - 1):
            if words[i] == a:
                next_word = words[i + 1]
                next_word_counts[next_word] = next_word_counts.get(next_word, 0) + 1

    if not next_word_counts:
        return None
    time.sleep(1)
    return max(next_word_counts, key=next_word_counts.get)

def generate_sentence(start_word, sentences, max_length=5):
    sentence = [start_word]
    for _ in range(max_length - 1):
        next_word = p_of_a_given_b(sentence[-1], sentences)
        if not next_word:
            break
        sentence.append(next_word)
    
    return " ".join(sentence)

@app.get("/predict")
def predict(word: str):
    generated_sentence = generate_sentence(word.lower(), sentences)
    return {"sentence": generated_sentence}
