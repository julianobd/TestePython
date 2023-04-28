from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class ReverseIntegersInput(BaseModel):
    number: int

class SentenceInput(BaseModel):
    sentence: str

class MatchMismatchInput(BaseModel):
    sentence1: str
    sentence2: str

@app.post("/ReverseIntegers")
def reverse_integers(input_data: ReverseIntegersInput):
    reversed_number = int(str(input_data.number)[::-1]) if input_data.number >= 0 else -int(str(-input_data.number)[::-1])
    return {"reversed": reversed_number}

@app.post("/AverageWordsLength")
def average_words_length(input_data: SentenceInput):
    words = re.findall(r'\b\w+\b', input_data.sentence)
    avg_length = sum(len(word) for word in words) / len(words)
    return {"average": round(avg_length, 2)}

@app.post("/MatchedMismatchedWords")
def matched_mismatched_words(input_data: MatchMismatchInput):
    words1 = set(re.findall(r'\b\w+\b', input_data.sentence1))
    words2 = set(re.findall(r'\b\w+\b', input_data.sentence2))

    matched_words = words1.intersection(words2)
    mismatched_words = words1.symmetric_difference(words2)

    return {"MatchedWords": list(matched_words), "MismatchedWords": list(mismatched_words)}