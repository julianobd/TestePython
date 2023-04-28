import pytest
import httpx
from main import app
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.asyncio
async def test_reverse_integers():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ReverseIntegers", json={"number": -543})
    assert response.status_code == 200
    assert response.json() == {"reversed": -345}

@pytest.mark.asyncio
async def test_average_words_length():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/AverageWordsLength", json={"sentence": "Olá, a todos! Testando a média de caracteres"})
    assert response.status_code == 200
    assert response.json() == {"average": 4.38}

@pytest.mark.asyncio
async def test_matched_mismatched_words():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/MatchedMismatchedWords", json={
            "sentence1": "We are really pleased to meet you in our city",
            "sentence2": "The city was hit by a really heavy storm"
        })
    assert response.status_code == 200
    assert set(response.json()["MatchedWords"]) == set(["really", "city"])
    assert set(response.json()["MismatchedWords"]) == set(['We', 'to', 'heavy', 'The', 'storm', 'meet', 'hit', 'pleased', 'are', 'by', 'a', 'in', 'was', 'you', 'our'])
