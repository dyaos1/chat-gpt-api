from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = OpenAI()

# cors middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NovelModel(BaseModel):
    characters: str
    news_text: str
    genre: str

def request_gpt_api(
    prompt: NovelModel,
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 500,
    temperature: float = 0.7 ,
)-> str:
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "당신은 촉망받는 소설가 입니다."},
            {"role": "user", "content": f"<등장인물>{prompt.characters}</등장인물><뉴스기사>{prompt.news_text}</뉴스기사> 를 소재로 장르가 {prompt.genre}인 소설을 써주세요."}
        ]
    )
    return completion.choices[0].message.content

@app.post("/test")
async def test(data: NovelModel):
    return request_gpt_api(data)
