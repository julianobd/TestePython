import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import re

app = FastAPI()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginInput(BaseModel):
    username: str
    password: str

class ReverseIntegersInput(BaseModel):
    number: int

class SentenceInput(BaseModel):
    sentence: str

class MatchMismatchInput(BaseModel):
    sentence1: str
    sentence2: str

class JWTBearer(HTTPBearer):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        super().__init__()

    async def __call__(self, credentials: HTTPAuthorizationCredentials):
        try:
            payload = jwt.decode(credentials.credentials, self.secret_key, algorithms=["HS256"])
            return credentials
        except (jwt.JWTError, AttributeError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
jwt_bearer = JWTBearer(secret_key=SECRET_KEY)

@app.post("/token", response_model=Token)
async def Login(login: LoginInput):
    # não fiz implementação de onde validará.. então.. tanto faz as credenciais..
    payload = {"sub": login.username}
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

def GetCurrentUser(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return username
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

@app.post("/ReverseIntegers")
def ReverseIntegers(input_data: ReverseIntegersInput, current_user: str = Depends(GetCurrentUser)):
    reversed_number = int(str(input_data.number)[::-1]) if input_data.number >= 0 else -int(str(-input_data.number)[::-1])
    return {"reversed": reversed_number}

@app.post("/AverageWordsLength")
def AverageWordsLength(input_data: SentenceInput, current_user: str = Depends(GetCurrentUser)):
    words = re.findall(r'\b\w+\b', input_data.sentence)
    avg_length = sum(len(word) for word in words) / len(words)
    return {"average": round(avg_length, 2)}

@app.post("/MatchedMismatchedWords")
def MatchedMismatchedWords(input_data: MatchMismatchInput, current_user: str = Depends(GetCurrentUser)):
    words1 = set(re.findall(r'\b\w+\b', input_data.sentence1))
    words2 = set(re.findall(r'\b\w+\b', input_data.sentence2))

    matched_words = words1.intersection(words2)
    mismatched_words = words1.symmetric_difference(words2)

    return {"MatchedWords": list(matched_words), "MismatchedWords": list(mismatched_words)}