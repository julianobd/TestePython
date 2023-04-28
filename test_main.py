import pytest
import httpx
from main import app
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
import jwt

client = TestClient(app)

async def get_access_token(client):
    username = "teste"
    password = "teste"

    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/Token", json={"username": "a", "password": "b"})

    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

@pytest.mark.asyncio
async def test_reverse_integers():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        token = await get_access_token(ac)
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.post("/ReverseIntegers", json={"number": -543}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"reversed": -345}

@pytest.mark.asyncio
async def test_average_words_length():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        token = await get_access_token(ac)
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.post("/AverageWordsLength", json={"sentence": "Olá, a todos! Testando a média de caracteres"}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"average": 4.38}

@pytest.mark.asyncio
async def test_matched_mismatched_words():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        token = await get_access_token(ac)
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.post("/MatchedMismatchedWords", json={
            "sentence1": "We are really pleased to meet you in our city",
            "sentence2": "The city was hit by a really heavy storm"
        }, headers=headers)
    assert response.status_code == 200
    assert set(response.json()["MatchedWords"]) == set(["really", "city"])
    assert set(response.json()["MismatchedWords"]) == set(['We', 'to', 'heavy', 'The', 'storm', 'meet', 'hit', 'pleased', 'are', 'by', 'a', 'in', 'was', 'you', 'our'])
